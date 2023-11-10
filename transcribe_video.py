import os
from tqdm import tqdm
import whisper
import numpy as np
from pathlib import Path
from pytube import YouTube
import random
import string

#@markdown Choose a Whisper model. `base` is the fastest and uses the least amount of memory.
#@param ["base", "small", "medium", "large"]
model_type = 'medium'  
   


class VideoRecognizer:
    def __init__(self,video_path,language,model_type='small',):
        print("MyClass instance created")
        #@markdown Where to save the video and subtitle.
        #@param {type: 'string'}
        self.save_path = 'output'  
        self.save_path = Path(self.save_path)
        self.save_path.mkdir(exist_ok=True, parents=True)
        self.video_path=video_path
        #@markdown What to name the saved video and subtitle.
        #@param {type: 'string'}
        self.filename = 'fishbrother'
        #@markdown Video Language Code
        #@param {type: 'string'}
        self.video_lang = language
        #@markdown Which format to save the subtitle in.
        #@param ["srt", "txt"]
        self.format = 'srt'
    def detectVideo(self):
        result, video, filename = self.transcribe()
        sub = self.convert_to_subtitle(result['segments'])
        sub_transcribed = self.save_subtitle(sub, self.save_path,filename+'-sub', format=format)
        

    def get_video_from_youtube_url(self,url, filename=None):
        yt = YouTube(url)
        video_file = str(self.save_path/f'{filename}.mp4')
        s = (yt.streams.filter(progressive=True, file_extension='mp4')
            .order_by('resolution').asc().first()
        )
        s.download(filename=video_file)
        return video_file


    def transcribe(self):
        if self.video_path.startswith('http') or 'youtube.com' in self.video_path:
            random_filename=self.generate_random_filename()
            print(f"Downloading Youtube Video {self.video_path}")
            video = self.get_video_from_youtube_url(url=self.video_path,filename=random_filename)
        else :
            print("Decode local video\n")
        print(f"Decode language {self.video_lang}.")
        options = whisper.DecodingOptions(fp16=False, language=self.video_lang)
        model = whisper.load_model(model_type)
        result = model.transcribe(video, **options.__dict__, verbose=False)
        if self.video_path.startswith('http') or 'youtube.com' in self.video_path:
            return result, video, random_filename    
        else :
            return result, video, self.filename
        


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


    def convert_to_subtitle(self,segs):
        if format == 'srt':
            sub = self.segments_to_srt(segs)
        elif format == 'txt':
            sub = self.transcribed_text(segs)
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

    def generate_random_filename(prefix="youtube",extension=".mp4"):
        """
        Generate a random filename with a specified extension.

        :param extension: File extension (default is .txt)
        :return: Random filename as a string
        """
        letters = string.ascii_lowercase
        filename = 'youtube'.join(random.choice(letters) for i in range(10))  # Generate a random string of length 10
        return f"{prefix}_{filename}{extension}"
    
    def setOutputFormat(self,output_format): # srt / txt
        self.format = output_format