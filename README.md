# OpenAI Transcribe Python Project
A project to transcribe video / audio using whisper model to subtitle files (txt, srt, vtt). The project also support text-to-text translation using facebook M2M100 model.

```
python3 -m venv .venv 
pip install -q git+https://github.com/openai/whisper.git
pip install -q pytube transformers sentencepiece tqdm
pip3 install -r requirements.txt

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

## How to run search.py?
```
python util/search.py E:/ericDrive/ mkv
```
doc:
https://pypi.org/project/openai/
pytube api doc: 
https://pytube.io/en/latest/index.html

suppport machine:
Mac (currently), python 3.10 (3.11 conflict with Whisper)
Window, python 3.10 or below