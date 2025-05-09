# Gemini APIでmp3から議事録を自動生成

## 概要
mp3音声ファイルをGoogle Gemini APIで直接処理し、議事録（要約）を自動生成するPythonスクリプトです。

## 必要要件
- Python 3.8以上
- Google Gemini APIのAPIキー（環境変数`GEMINI_API_KEY_FOR_MINUTES`に設定）
- `prompt.md`（スクリプトと同じディレクトリに配置）

## インストール

1. 仮想環境(venv)の作成・有効化

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windowsの場合: .venv\Scripts\activate
```

2. 必要パッケージのインストール

```bash
pip install -r requirements.txt
```

## 使い方

1. 仮想環境(venv)を有効化

```bash
source .venv/bin/activate  # Windowsの場合: .venv\Scripts\activate
```

2. スクリプトを実行

```bash
python createMinuteByGemini.py 入力ファイル.mp3
```
- 入力mp3ファイルと同じディレクトリ・同じファイル名（拡張子のみ.txt）で議事録が出力されます。

## 注意事項
- mp3ファイルは20MB未満推奨（Gemini APIの制限に注意）
- Gemini APIの仕様上、英語以外の音声認識精度は保証されません。
- API利用料・トークン制限にご注意ください。
- prompt.mdの内容が議事録生成のプロンプトとして使われます。

## 依存パッケージ
- google-generativeai