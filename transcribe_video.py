import os
from tqdm import tqdm
import whisper
import numpy as np
from pathlib import Path
from pytube import YouTube
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
import random
import string
import requests
import torch
import gc
from contextlib import contextmanager
from subtitle_generator import YoutubeProcessor
from subtitle_generator import VideoProcessor

@contextmanager
def use_whisper_model(model_type,device):
    model = whisper.load_model(model_type, device=device)
    try:
        yield model
    finally:
        del model
        gc.collect()
@contextmanager
def use_m2m100_model(device):
    model_name = "facebook/m2m100_1.2B"
    tokenizer = M2M100Tokenizer.from_pretrained(model_name)
    m2m100_model = M2M100ForConditionalGeneration.from_pretrained(model_name).to(device)
    try:
        yield m2m100_model, tokenizer
    finally:
        del m2m100_model
        gc.collect()

class VideoRecognizer:
    
    
    def __init__(self,video_path, source_language='zh', target_language=None, output_dir='output',output_filename = None, model_type='small',):
        print("VideoRecognizer instance created")
        # Ensure a GPU is available
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"use device: {self.device}")
        
        self.output_dir = Path(output_dir) if output_dir else Path("output")
        self.output_dir.mkdir(exist_ok=True, parents=True)
        print(self.output_dir)
        self.video_path = video_path
        self.source_language = source_language
        self.target_language = target_language
        self.model_type = model_type  
        if output_filename:
            self.outputFilename = output_filename
        else:
            filename_without_extension = os.path.splitext(os.path.basename(video_path))[0]
            self.outputFilename = filename_without_extension
        self.output_format_list = []
        self.suffix = target_language if target_language else source_language

        
    def detectVideo(self):
        result, video, item_count = self.transcribe()
        print(f"Translation items count: {item_count}")
        sub = self.convert_to_subtitle(result['segments'])

    def get_video_from_youtube_url(self,url, filename=None):
        yt = YouTube(url)
        video_file = str(self.output_dir/f'{filename}.mp4')
        s = (yt.streams.filter(progressive=True, file_extension='mp4')
            .order_by('resolution').asc().first()
        )
        s.download(filename=video_file)
        return video_file
    def download_facebook_video(self,video_url, filename=None):
        response = requests.get(video_url, stream=True)
        video_file = str(self.output_dir/f'{filename}.mp4')
        with open(video_file, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024): 
                if chunk:
                    file.write(chunk)
    def translate(self,text ,model, tokenizer ,src_lang="ja", tgt_lang="zh"):
        tokenizer.src_lang = src_lang
        encoded = tokenizer(text, return_tensors="pt").to(self.device)
        generated_tokens = model.generate(**encoded, forced_bos_token_id=tokenizer.get_lang_id(tgt_lang))
        return tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
    def transcribe(self):
        if 'youtube.com' in self.video_path:
            ytProcessor = YoutubeProcessor()
            video = ytProcessor.download_video(url=self.video_path)
        elif 'facebook.com' in self.video_path:
            random_filename=self.generate_random_filename(prefix="facebook")
            print(f"Downloading Facebook Video {self.video_path} into {random_filename}")
            video = self.download_facebook_video(video_url=self.video_path,filename=random_filename)
        else :
            print("Decode local video\n")
            if not os.path.exists(self.video_path):
                raise ValueError(f"The provided video path does not exist: {video_path}")
            source_folder = os.path.dirname(self.video_path)
            filename_with_extension = os.path.basename(self.video_path)
            filename_without_extension, _ = os.path.splitext(filename_with_extension)
            
            print(f"filename_with_extension {filename_with_extension}")
            video = source_folder+'/'+filename_with_extension
        print(f"Decode source language {self.source_language}.")
        vp = VideoProcessor()
        audio_path = vp.convert_video_to_audio(video,"aac")

        with use_whisper_model(self.model_type,self.device) as whisper_model:
            options = whisper.DecodingOptions(fp16=False, language=self.source_language)
            result = whisper_model.transcribe(audio_path, **options.__dict__, verbose=False)
            pass
        # Translate if need
        if (self.target_language==None or self.source_language.lower() == self.target_language.lower()):
            return result, audio_path, 0
        segments = result['segments']
        translate_item_count = 0  # Initialize the item count
        with use_m2m100_model(self.device) as (m100_model, token):

            # Iterate over each segment
            for segment in segments:
                original_text = segment['text']

                modified_text = self.translate(original_text, m100_model, token, self.source_language.lower(), self.target_language.lower())

                segment['text'] = modified_text
                start_time = segment["start"]
                end_time = segment["end"]
                print(f"origin: {original_text} --> new: {modified_text}, start {start_time} -- {end_time}")
                translate_item_count += 1
            pass
        return result, audio_path, translate_item_count

    def segments_to_srt(self, segs):
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
    def segments_to_vtt(self, segs):
        text = ["WEBVTT"]
        text.append("")  # Empty line after header

        for i, s in enumerate(segs):
            # VTT uses the same numbering as SRT for segments
            text.append(str(i + 1))

            # Start time formatting
            time_start = s['start']
            hours, minutes, seconds = int(time_start / 3600), int((time_start / 60) % 60), time_start % 60
            timestamp_start = "%02d:%02d:%06.3f" % (hours, minutes, seconds)

            # End time formatting
            time_end = s['end']
            hours, minutes, seconds = int(time_end / 3600), int((time_end / 60) % 60), time_end % 60
            timestamp_end = "%02d:%02d:%06.3f" % (hours, minutes, seconds)

            # Adding the formatted timestamps and text
            text.append(timestamp_start + " --> " + timestamp_end)
            text.append(s['text'].strip())
            text.append("")  # Empty line after each segment

        return "\n".join(text)

    def convert_to_subtitle(self, segs):
        if 'srt' in self.output_format_list:
            sub = self.segments_to_srt(segs)
            self.save_subtitle(sub, self.output_dir,f"{self.outputFilename}-{self.suffix}", format='srt')
        if 'vtt' in self.output_format_list:
            sub = self.segments_to_vtt(segs)
            self.save_subtitle(sub, self.output_dir,f"{self.outputFilename}-{self.suffix}", format='vtt')
        if 'txt' in self.output_format_list:
            sub = self.transcribed_text(segs)
            self.save_subtitle(sub, self.output_dir,f"{self.outputFilename}-{self.suffix}", format='txt')
        return sub
        

    def save_subtitle(self,sub, output_dir, filename, format='srt'):
        srt_file = output_dir/f'{filename}.{format}'
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
    
    def add_text_output(self):
        self.output_format_list.append('txt')
    def add_srt_output(self):
        self.output_format_list.append('srt')
    def add_vtt_output(self):
        self.output_format_list.append('vtt')