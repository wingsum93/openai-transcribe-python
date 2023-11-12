pipenv run python app.py

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
```
python3
python transcribe-video-cli.py --video_path "VIDEO_URL_OR_PATH" --model_type "MODEL_TYPE" --lang "Language"

python3 transcribe-video-cli.py --video_path "https://www.youtube.com/watch?v=UYEXT0uhFLw" --lang=zh
python3 transcribe-video-cli.py --video_path "https://www.youtube.com/watch?v=Nk2_1e6QglI" --lang=ja

```


feature ref:
https://github.com/AssemblyAI-Examples/whisper-multilingual/blob/main/main.py


run with out activate the env:



doc:
https://pypi.org/project/openai/

suppport machine:
Mac (currently), python 3.10 (3.11 conflict with Whisper)
Window (not yet support)