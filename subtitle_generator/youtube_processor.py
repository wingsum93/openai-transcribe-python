from pytube import YouTube
from pytube.exceptions import PytubeError
from logger import Logger
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
            yt = YouTube(
                url,
                use_oauth=True,
                allow_oauth_cache=True
                )
            video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            print(video)
            if not video:
                raise Exception("No youtube video stream found")

            video_path = video.download(self.download_folder)
            self.logger.logEndAction('download yt')
            return video_path
        except PytubeError as e:
            print(f"An error occurred: {e}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None