import os
import sys
import subprocess
import tempfile
import whisper

# ffmpeg を使って MP3/M4A を一時的な WAV ファイルに変換する関数
def convert_to_temp_wav(input_path):
    # 拡張子チェック（MP3 または M4A のみ対応）
    ext = os.path.splitext(input_path)[1].lower()
    if ext not in [".mp3", ".m4a"]:
        raise ValueError("対応している形式は MP3 または M4A のみです。")

    # 一時ファイルを作成（拡張子 .wav）
    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    temp_wav_path = temp_wav.name
    temp_wav.close()  # ffmpeg が書き込めるように閉じる

    # ffmpeg コマンドで変換
    command = [
        "ffmpeg",
        "-y",  # 既存ファイルがあれば上書き
        "-i", input_path,  # 入力ファイル
        temp_wav_path  # 出力ファイル（一時）
    ]

    try:
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print("❌ ffmpeg による変換に失敗しました。")
        raise e

    return temp_wav_path

# Whisper を使って文字起こしを行い、TXT に保存する関数
def transcribe_and_save(temp_wav_path, output_txt_path):
    # Whisper モデルを読み込み（"base", "medium", "large" など選択可能）
    model = whisper.load_model("base")

    # 言語を明示（日本語の場合 "ja"、英語の場合 "en"）
    result = model.transcribe(temp_wav_path, language="ja")

    # 結果をテキストファイルに保存
    with open(output_txt_path, "w", encoding="utf-8") as f:
        f.write(result["text"])

    print(f"✅ 文字起こし完了: {output_txt_path}")

    # 一時ファイルを削除
    os.remove(temp_wav_path)

# メイン関数：コマンドライン引数から音声ファイルを受け取り、処理を実行
def main():
    if len(sys.argv) != 2:
        print("使い方: python transcribe_temp.py 音声ファイル.mp3/m4a")
        return

    input_path = sys.argv[1]
    output_txt_path = os.path.splitext(input_path)[0] + ".txt"

    # 一時 WAV ファイルに変換
    temp_wav_path = convert_to_temp_wav(input_path)

    # Whisper で文字起こしし、結果を保存
    transcribe_and_save(temp_wav_path, output_txt_path)

if __name__ == "__main__":
    main()