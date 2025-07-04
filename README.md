#  🎧 OpenAI Transcribe Python Project
> A powerful CLI tool to transcribe and translate audio/video content into subtitles (`.srt`, `.vtt`, `.txt`) using OpenAI Whisper and Facebook M2M100.

---
## ✅ Features

- 🎤 **Voice Recording** from mic, auto-transcribed
- 📼 **Transcribe local files** (`.mp4`, `.aac`, `.wav`, etc.)
- 📺 **Download & transcribe YouTube or Facebook videos**
- 🌍 **Translate** to other languages (e.g. zh → en) using Facebook M2M100
- 📁 **Batch processing** for local/YT lists
- 📄 Outputs: `.srt`, `.vtt`, `.txt`
- 💬 Full CLI interface with rich options
- 🇭🇰 Logger speaks fluent Cantonese 😎

---

## 🚀 Quick Start

### 1. Install

```bash
git clone https://github.com/yourname/openai-transcribe-python.git
cd openai-transcribe-python

python3 -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

pip install -r requirements.txt
```
```bash
python3 -m venv .venv 
pip install -q git+https://github.com/openai/whisper.git
pip install -q pytube transformers sentencepiece tqdm

pip3 install -U openai-whisper
mac pytouch:
pip3 install torch torchvision torchaudio
window cuda command
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

feature ref:
https://github.com/AssemblyAI-Examples/whisper-multilingual/blob/main/main.py


## How to run the program?
[Run program](doc/command.md)
## Test Installation
```bash
stt --help
```

## Example Usage
🎙️ Record from Mic
```bash
stt record --source zh --target en --model medium --txt --srt
```
> Speak and type end to stop. It transcribes + translates your voice.
### 📼 Local File (Audio or Video)
```bash
stt transcribe local \
  --file sample/canton_long.mp3 \
  --source zh --target en \
  --model medium \
  --srt --txt

```
### 📺 YouTube
```bash
stt transcribe youtube \
  --url https://youtu.be/abc123 \
  --source en --target zh \
  --model medium \
  --srt --txt
```
### 🧑‍🤝‍🧑 Facebook Video
```bash
stt transcribe facebook \
  --url https://www.facebook.com/watch?v=xyz \
  --source zh --target en \
  --model medium \
  --txt --srt
```
### 📂 Batch List
```bash
stt transcribe-many \
  --file temp/mixed-files.txt \
  --source zh \
  --target en \
  --model medium \
  --txt --srt
```

## 🧪 Testing
```bash
pytest tests/
```

## 📁 Project Structure

subtitle_generator/
├── cli_main.py       # CLI entry point (Click-based)
├── processor.py      # Transcription logic
├── recorder.py       # Microphone recording
├── video_processor.py
├── youtube_processor.py
├── facebook_processor.py
├── subtitle_generator.py
├── text_translator.py
├── logger.py         # Cantonese logger ❤️
### 📦 Supported Input Formats
- Audio: .aac, .m4a, .wav, .mp3
- Video: .mp4, .mkv, .mov
- URL: YouTube, Facebook
## 🧠 Notes
- Whisper works best with Python 3.10
- For FB/YT, yt-dlp and ffmpeg are required
- Translation requires internet (for Facebook M2M100)

# ❤️ Credits
Built with Whisper, Transformers, and love.

---

## ✅ What’s Improved

- Cleaner layout with icons for readability
- Clear command examples
- Proper sectioning: install, usage, format support
- Credit + license section
- Cantonese pride 🇭🇰
