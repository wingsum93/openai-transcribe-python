from pytube import YouTube
from pytube.exceptions import PytubeError
import os

class YoutubeProcessor:
    def __init__(self, download_folder="downloads"):
        self.download_folder = download_folder
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

    def download_video(self, url):
        try:
            yt = YouTube(url)
            video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            if not video:
                raise Exception("No suitable video stream found")

            video_path = video.download(self.download_folder)
            return video_path
        except PytubeError as e:
            print(f"An error occurred: {e}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None