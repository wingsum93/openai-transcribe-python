import os
from tqdm import tqdm
import whisper
import numpy as np
from pathlib import Path
from pytube import YouTube
import random
import string
import requests

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
        self.format = "srt"
        #@markdown Choose a Whisper model. `base` is the fastest and uses the least amount of memory.
        #@param ["base", "small", "medium", "large"]
        self.model_type = model_type  
        self.outputFilename = ''
    def detectVideo(self):
        result, video = self.transcribe()
        sub = self.convert_to_subtitle(result['segments'])
        sub_transcribed = self.save_subtitle(sub, self.save_path,self.outputFilename+'-sub', format=self.format)
        

    def get_video_from_youtube_url(self,url, filename=None):
        yt = YouTube(url)
        video_file = str(self.save_path/f'{filename}.mp4')
        s = (yt.streams.filter(progressive=True, file_extension='mp4')
            .order_by('resolution').asc().first()
        )
        s.download(filename=video_file)
        return video_file
    def download_facebook_video(self,video_url, filename=None):
        response = requests.get(video_url, stream=True)
        video_file = str(self.save_path/f'{filename}.mp4')
        with open(video_file, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024): 
                if chunk:
                    file.write(chunk)

    def transcribe(self):
        if 'youtube.com' in self.video_path:
            random_filename=self.generate_random_filename()
            print(f"Downloading Youtube Video {self.video_path} into {random_filename}")
            video = self.get_video_from_youtube_url(url=self.video_path,filename=random_filename)
        elif 'facebook.com' in self.video_path:
            random_filename=self.generate_random_filename(prefix="facebook")
            print(f"Downloading Facebook Video {self.video_path} into {random_filename}")
            video = self.download_facebook_video(video_url=self.video_path,filename=random_filename)
        else :
            print("Decode local video\n")
            self.outputFilename ='gg'
            filename_with_extension = os.path.basename(self.video_path)
            filename_without_extension, _ = os.path.splitext(filename_with_extension)
            self.outputFilename = filename_without_extension
        print(f"Decode language {self.video_lang}.")
        options = whisper.DecodingOptions(fp16=False, language=self.video_lang)
        model = whisper.load_model(self.model_type)
        result = model.transcribe(video, **options.__dict__, verbose=False)
        return result, video
        


    def segments_to_srt(self,segs):
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
        if self.format == 'srt':
            sub = self.segments_to_srt(segs)
        elif self.format == 'txt':
            sub = self.transcribed_text(segs)
        else:
            raise ValueError(f"format {self.format} is not supported!")
        return sub
        

    def save_subtitle(self,sub, save_path, filename, format='srt'):
        srt_file = save_path/f'{filename}.{format}'
        print(f"Output text file: {srt_file}")
        with open(srt_file, 'w', encoding="utf-8") as f:
            f.write(sub)
        return srt_file


    def transcribed_text(self,segs):
        texts = [s['text'] for s in segs]
        text = '\n'.join(texts)
        return text

    def generate_random_filename(self,prefix="youtube"):
        """
        Generate a random filename with a specified extension.

        :param extension: File extension (default is .txt)
        :return: Random filename as a string
        """
        letters = string.ascii_lowercase
        filename = ''.join(random.choice(letters) for i in range(10))  # Generate a random string of length 10
        self.outputFilename = f"{prefix}_{filename}"
        return self.outputFilename
    
    def setOutputFormat(self,output_format): # srt / txt
        self.format = output_format