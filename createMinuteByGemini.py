import os
from pydub import AudioSegment, silence
import google.generativeai as genai
from tqdm import tqdm

# === 設定 ===
API_KEY = os.getenv('GEMINI_API_KEY_FOR_MINUTES')  # 環境変数からAPIキー取得
MODEL_NAME = "gemini-2.5-flash-preview-04-17"
CHUNK_LENGTH_MS = 10 * 60 * 1000  # 10分（ミリ秒）
SILENCE_THRESH = -40  # 無音判定閾値（dB）
MIN_SILENCE_LEN = 1000  # 無音区間の最小長さ（ms）

# === mp3分割 ===
def split_audio(input_mp3, out_dir):
    audio = AudioSegment.from_mp3(input_mp3)
    chunks = silence.split_on_silence(
        audio,
        min_silence_len=MIN_SILENCE_LEN,
        silence_thresh=SILENCE_THRESH,
        keep_silence=500
    )
    # チャンクを10分以内でまとめる
    merged_chunks = []
    current = AudioSegment.empty()
    for chunk in chunks:
        if len(current) + len(chunk) > CHUNK_LENGTH_MS:
            merged_chunks.append(current)
            current = chunk
        else:
            current += chunk
    if len(current) > 0:
        merged_chunks.append(current)
    # ファイル保存
    os.makedirs(out_dir, exist_ok=True)
    chunk_files = []
    for i, chunk in enumerate(merged_chunks):
        path = os.path.join(out_dir, f"chunk_{i+1}.mp3")
        chunk.export(path, format="mp3")
        chunk_files.append(path)
    return chunk_files

# === Gemini APIで音声→テキスト ===
def transcribe_mp3(mp3_path):
    uploaded_file = genai.upload_file(mp3_path)
    model = genai.GenerativeModel(MODEL_NAME)
    prompt = 'Generate a transcript of the speech.'
    response = model.generate_content([prompt, uploaded_file])
    return response.text

# === 議事録生成 ===
def generate_minutes(transcript):
    prompt_file = os.path.join(os.path.dirname(__file__), "prompt.md")
    if not os.path.exists(prompt_file):
        raise FileNotFoundError(f"プロンプトファイルが見つかりません: {prompt_file}")
    with open(prompt_file, 'r', encoding='utf-8') as f:
        prompt = f.read().strip()
    model = genai.GenerativeModel(MODEL_NAME)
    full_prompt = prompt + "\n" + transcript
    response = model.generate_content([full_prompt])
    return response.text

# === メイン処理 ===
def main(input_mp3):
    genai.configure(api_key=API_KEY)
    chunk_dir = "chunks"
    print("音声ファイルを分割中...")
    chunk_files = split_audio(input_mp3, chunk_dir)
    print(f"{len(chunk_files)}個のチャンクに分割されました。")
    transcripts = []
    for f in tqdm(chunk_files, desc="音声→テキスト変換"):
        text = transcribe_mp3(f)
        transcripts.append(text)
    full_transcript = "\n".join(transcripts)
    print("議事録を生成中...")
    minutes = generate_minutes(full_transcript)
    # 出力ファイル名とパスをmp3と同じにする
    mp3_dir = os.path.dirname(input_mp3)
    mp3_base = os.path.splitext(os.path.basename(input_mp3))[0]
    txt_path = os.path.join(mp3_dir, mp3_base + ".txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(minutes)
    print(f"{txt_path} に議事録を出力しました。")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("使い方: python createMinuteByGemini.py 入力mp3ファイル")
        exit(1)
    main(sys.argv[1])
