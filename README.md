# Gemini APIでmp3から議事録を自動生成

## 概要
mp3音声ファイルをGoogle Gemini APIでテキスト化し、議事録（要約）を自動生成するPythonスクリプトです。

## 必要要件
- Python 3.8以上
- Google Gemini APIのAPIキー（環境変数`GEMINI_API_KEY_FOR_MINUTES`に設定）

## インストール
```bash
pip install -r requirements.txt
```

## 使い方
```bash
python createMinuteByGemini.py 入力ファイル.mp3
```
- `minutes.txt` に議事録が出力されます。
- `chunks/` ディレクトリに分割された音声ファイルが一時保存されます。

## 注意事項
- 長時間音声は自動で10分ごとに分割されます。
- Gemini APIの仕様上、英語以外の音声認識精度は保証されません。
- API利用料・トークン制限にご注意ください。

## 依存パッケージ
- google-generativeai
- pydub
- tqdm

## ライセンス
MIT 