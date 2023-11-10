pipenv run python app.py

```
python3 -m venv .venv 
!pip install -q git+https://github.com/openai/whisper.git
!pip install -q pytube transformers sentencepiece tqdm 

pip3 install -U openai-whisper
pip3 install -U pytube
```
```
python3
python transcribe-video-cli.py --video_path "VIDEO_URL_OR_PATH" --model_type "MODEL_TYPE"

python3 transcribe-video-cli.py --video_path "https://www.youtube.com/watch?v=YdJrQGM3_a0"
```




run with out activate the env:



doc:
https://pypi.org/project/openai/
