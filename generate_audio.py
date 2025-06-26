from gtts import gTTS
import sys
import os

def generate_audio(text, filename, out_dir="../midori-audio/public/audios"):
    os.makedirs(out_dir, exist_ok=True)
    filepath = os.path.join(out_dir, filename)
    tts = gTTS(text, lang="ja")
    tts.save(filepath)

if __name__ == "__main__":
    text = sys.argv[1]
    filename = sys.argv[2]
    generate_audio(text, filename)
