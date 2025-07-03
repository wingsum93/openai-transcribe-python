#from pytube import YouTube
#from pytube.exceptions import PytubeError
from .logger import Logger
from pytubefix import YouTube
from pytubefix.cli import on_progress
import os
import json

class YoutubeProcessor:
    def __init__(self, logger = Logger(),download_folder="downloads"):
        print(f"download folder: {download_folder}")
        self.download_folder = download_folder
        self.logger = logger
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

    def download_video(self, url):
        try:
            self.logger.logStartAction('download yt')
            yt = YouTube(url, on_progress_callback=on_progress)
            print(yt.title)
            ys = yt.streams.get_audio_only()
            file_path = ys.download(
                output_path=self.download_folder,
                filename_prefix='audio_'
            )
            self.logger.logEndAction('download yt')
            return file_path
        
        except Exception as e:
            print(f"An error occurred: {e}")
            return None