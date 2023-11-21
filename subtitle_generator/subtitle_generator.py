import os
import copy
from tqdm import tqdm
from contextlib import contextmanager
import whisper
import torch
import gc
from pathlib import Path
from text_translator import TextTranslator

@contextmanager
def use_whisper_model(model_type, device):
    model = whisper.load_model(model_type, device=device)
    try:
        yield model
    finally:
        del model
        if device == 'cuda':
            torch.cuda.empty_cache()  # Clear memory cache if the device is CUDA
        gc.collect()

class SubtitleGenerator:
    def __init__(self, 
                audio_file_path:str, 
                source_language:str, 
                target_language:str, 
                output_dir:str, 
                output_filename=None, 
                auto_decide_output_name=True, 
                model_type:str='small', 
                confident_level=0.4):
        self.audio_file_path = audio_file_path
        self.source_language = source_language
        self.target_language = target_language
        self.confident_level = confident_level
        self.model_type = model_type  # Add model_type as an instance attribute
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

        self.output_format_list = []
        self.output_dir = Path(output_dir) if output_dir else Path("output")
        self.output_dir.mkdir(exist_ok=True, parents=True)
        if not auto_decide_output_name:
            self.output_filename = output_filename
        else:
            filename_without_extension = os.path.splitext(os.path.basename(audio_file_path))[0]
            self.output_filename = filename_without_extension

    def generate_subtitles(self):
        result = self.transcribe_audio_to_segment(self.audio_file_path)
        segments = result['segments']
        # Batch filter for high confident segments
        # segments = [segment for segment in segments if segment['confidence'] > self.confident_level]

        # Translation (if required)
        need_translation = bool(self.target_language and self.target_language != self.source_language)
        if need_translation:
            translator = TextTranslator()
            translated_segments = copy.deepcopy(segments)
            translator.translate(translated_segments, self.source_language, self.target_language)

        
        self.convert_to_subtitle(segments, 
                                 self.output_dir, 
                                 self.output_filename,
                                 self.source_language)
        if need_translation:
            self.convert_to_subtitle(translated_segments, 
                                 self.output_dir, 
                                 self.output_filename,
                                 self.target_language)
        return

    def transcribe_audio_to_segment(self, audio_path):
        # Now an instance method, not a static method
        with use_whisper_model(self.model_type, self.device) as whisper_model:
            options = whisper.DecodingOptions(fp16=False, language=self.source_language)
            result = whisper_model.transcribe(audio_path, **options.__dict__, verbose=False)
        return result

    # Additional methods can be added here.

    def convert_to_subtitle(self, segs:list, output_dir:str, output_filename:str, suffix:str):
        if 'srt' in self.output_format_list:
            sub = self.segments_to_srt(segs)
            self.save_subtitle(sub, output_dir,f"{output_filename}-{suffix}", format='srt')
        if 'vtt' in self.output_format_list:
            sub = self.segments_to_vtt(segs)
            self.save_subtitle(sub, output_dir,f"{output_filename}-{suffix}", format='vtt')
        if 'txt' in self.output_format_list:
            sub = self.transcribed_text(segs)
            self.save_subtitle(sub, output_dir,f"{output_filename}-{suffix}", format='txt')
        return sub
    
    def segments_to_srt(self, segs:list):
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
    
    def segments_to_vtt(self, segs:list):
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
    
    def transcribed_text(self,segs:list):
        texts = [s['text'] for s in segs]
        text = '\n'.join(texts)
        return text
    
    def save_subtitle(self,sub, output_dir, filename, format='srt'):
        srt_file = output_dir/f'{filename}.{format}'
        print(f"Output text file: {srt_file}")
        with open(srt_file, 'w', encoding="utf-8") as f:
            f.write(sub)
        return srt_file
    
    def add_text_output(self):
        self.output_format_list.append('txt')
    def add_srt_output(self):
        self.output_format_list.append('srt')
    def add_vtt_output(self):
        self.output_format_list.append('vtt')