# Overview
- mp3 or m4vのファイルの音声（日本語 or 英語）を文字起こししてtxtファイルとして出力します
- OpenAIの高精度音声認識モデルであるwhisperを使用します


# Requirements
- Python 3.13
- pip install openai-whisper pydub ffmpeg-python
#### ffmpeg も必要です。以下でインストールできます：
- macOS: brew install ffmpeg
- Ubuntu: sudo apt install ffmpeg
- Windows: FFmpeg公式サイトからダウンロードし、パスを通します

# Usage
- 実行pyファイルと音声ファイル（例：sample.mp3）を同じディレクトリに置きます
- python app.py sample.mp3
- 文字起こしされたtxtファイルが同ディレクトリに出力されます

# Supplement
- Whisperは日本語・英語を自動判別できますが、language="ja"やlanguage="en"で明示すると精度の上がる場合があります
- 長時間音声の場合は "medium" や "large" モデルの使用を検討してください（要GPU）

# Other
Whisperは内部的にWAV形式の音声データを扱いやすいため、
MP3やM4Aの圧縮形式をWAVに変換してから読み込みます


