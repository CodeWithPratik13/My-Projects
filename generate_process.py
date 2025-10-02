import os
import time
import subprocess
from text_to_audio import text_to_speech_file

def text_to_audio(folder):
    try:
        with open(f"user_upload/{folder}/desc.txt", encoding="utf-8") as f:
            text = f.read().strip()
        text_to_speech_file(text, folder)
        return True
    except Exception as e:
        print(f"❌ TTS failed for {folder}: {e}")
        return False

def create_reel(folder):
    command = f'''ffmpeg -f concat -safe 0 -i user_upload/{folder}/input.txt \
-i user_upload/{folder}/audio.mp3 \
-vf "scale=w=1080:h=1920:force_original_aspect_ratio=decrease,\
pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" \
-c:v libx264 -c:a aac -shortest -r 30 -pix_fmt yuv420p \
static/reels/{folder}.mp4'''
    try:
        subprocess.run(command, shell=True, check=True, stderr=subprocess.PIPE)
        print(f"✅ Reel created: static/reels/{folder}.mp4")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg failed for {folder}: {e.stderr.decode(errors='ignore')}")
        return False

if __name__ == "__main__":
    os.makedirs("static/reels", exist_ok=True)
    if not os.path.exists("done.txt"):
        open("done.txt", "w").close()

    while True:
        print("🔄 Processing queue...")
        with open("done.txt", "r") as f:
            done_folders = [line.strip() for line in f.readlines()]

        folders = os.listdir("user_upload")
        for folder in folders:
            if folder not in done_folders:
                if text_to_audio(folder) and create_reel(folder):
                    with open("done.txt", "a") as f:
                        f.write(folder + "\n")
        time.sleep(4)
