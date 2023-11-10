import os
from tqdm import tqdm
import whisper
import numpy as np
from pathlib import Path
from pytube import YouTube


#@markdown If `video_path` is a YouTube link, the video will be downloaded at the `save_path`.
#@param {type: 'string'}
video_path = 'https://www.youtube.com/watch?v=WqMw0WABxOs' 
#@markdown Choose a Whisper model. `base` is the fastest and uses the least amount of memory.
#@param ["base", "small", "medium", "large"]
model_type = 'medium'  
#@markdown Video Language Code
#@param {type: 'string'}
video_lang = 'zh'   
#@markdown Where to save the video and subtitle.
#@param {type: 'string'}
save_path = 'data'  
save_path = Path(save_path)
save_path.mkdir(exist_ok=True, parents=True)
#@markdown What to name the saved video and subtitle.
#@param {type: 'string'}
filename = 'fishbrother'
#@markdown Which format to save the subtitle in.
#@param ["srt", "txt"]
format = 'srt'



def get_video_from_youtube_url(url, save_path=None, filename=None):
    yt = YouTube(url)
    video_file = str(save_path/f'{filename}.mp4')
    s = (yt.streams.filter(progressive=True, file_extension='mp4')
         .order_by('resolution').desc().first()
    )
    s.download(filename=video_file)
    return video_file


def transcribe(video, save_path, filename, model_type='small'):
    if video.startswith('http'):
        print("Downloading Youtube Video\n")
        video = get_video_from_youtube_url(video, save_path=save_path, filename=filename
        )
    options = whisper.DecodingOptions(fp16=False, language=video_lang)
    model = whisper.load_model(model_type)
    result = model.transcribe(video, **options.__dict__, verbose=False)
    return result, video


def segments_to_srt(segs):
    text = []
    for i,s in tqdm(enumerate(segs)):
        text.append(str(i+1))

        time_start = s['start']
        hours, minutes, seconds = int(time_start/3600), (time_start/60) % 60, (time_start) % 60
        timestamp_start = "%02d:%02d:%06.3f" % (hours, minutes, seconds)
        timestamp_start = timestamp_start.replace('.',',')     
        time_end = s['end']
        hours, minutes, seconds = int(time_end/3600), (time_end/60) % 60, (time_end) % 60
        timestamp_end = "%02d:%02d:%06.3f" % (hours, minutes, seconds)
        timestamp_end = timestamp_end.replace('.',',')        
        text.append(timestamp_start + " --> " + timestamp_end)

        text.append(s['text'].strip() + "\n")
            
    return "\n".join(text)


def convert_to_subtitle(segs):
    if format == 'srt':
        sub = segments_to_srt(segs)
    elif format == 'txt':
        sub = transcribed_text(segs)
    else:
        raise ValueError(f"format {format} is not supported!")
    return sub
    

def save_subtitle(sub, save_path, filename, format='srt'):
    srt_file = save_path/f'{filename}.{format}'
    with open(srt_file, 'w') as f:
        f.write(sub)
    return srt_file


def transcribed_text(segs):
    texts = [s['text'] for s in segs]
    text = '\n'.join(texts)
    return text


print("Loading the model")
model = whisper.load_model(f'{model_type}')
print("Transcribing")
result, video = transcribe(video_path, save_path, filename, model_type=model_type)
sub = convert_to_subtitle(result['segments'])
sub_transcribed = save_subtitle(sub, save_path, filename+'-sub', format=format)
print(f"\n\nsubtitle is saved at {sub_transcribed}")