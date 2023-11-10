
import argparse
import os
from tqdm import tqdm
import whisper
import numpy as np
from pathlib import Path
from pytube import YouTube
import transcribe_video

def main(video_path, model_type,language):
    # Check if the video_path is a YouTube URL
    if 'youtube.com' in video_path:
        # Download the video using pytube
        print(f"Downloading video from {video_path}")
        # ... Code to download the video ...

    # Load the Whisper model
    print(f"Loading Whisper model: {model_type}")
    # ... Code to load and use the Whisper model ...
    model = whisper.load_model(f'{model_type}')
    result, video = transcribe_video.transcribe(video_path, transcribe_video.save_path, transcribe_video.filename,language=language, model_type=model_type)
    sub = transcribe_video.convert_to_subtitle(result['segments'])
    sub_transcribed = transcribe_video.save_subtitle(sub, transcribe_video.save_path, transcribe_video.filename+'-sub', format=format)
    print(f"\n\nsubtitle is saved at {sub_transcribed}")
    print("Transcription complete!")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Transcribe a video using OpenAI Whisper.')
    parser.add_argument('--video_path', type=str, required=True, help='The path to the video file or a YouTube URL.')
    parser.add_argument('--model_type', type=str, choices=['base', 'small', 'medium', 'large'], default='medium', help='The type of Whisper model to use.')
    parser.add_argument('--lang', type=str, choices=['zh', 'en', 'ja'], required=True, help='The type of language that video use.')

    args = parser.parse_args()
    main(args.video_path, args.model_type,args.lang)
