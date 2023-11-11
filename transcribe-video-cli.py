
import argparse
import os
from tqdm import tqdm
import whisper
import numpy as np
from pathlib import Path
from pytube import YouTube
from transcribe_video import VideoRecognizer

def main(video_path, model_type,language):

    vr1 = VideoRecognizer(video_path=video_path, language=language, model_type=model_type)
    vr1.detectVideo()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Transcribe a video using OpenAI Whisper.')
    parser.add_argument('--video_path', type=str, required=True, help='The path to the video file or a YouTube URL.')
    parser.add_argument('--model_type', type=str, choices=['tiny','base', 'small', 'medium', 'large','large-v2','large-v3'], default='small', help='The type of Whisper model to use.')
    parser.add_argument('--lang', type=str, choices=['zh', 'en', 'ja'], required=True, help='The type of language that video use.')

    args = parser.parse_args()
    main(args.video_path, args.model_type,args.lang)
