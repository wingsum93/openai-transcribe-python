#from pytube import YouTube
#from pytube.exceptions import PytubeError
from .logger import Logger
import yt_dlp
import os
import json

class YoutubeProcessor:
    def __init__(self, logger = Logger(),download_folder="downloads"):
        print(f"download folder: {download_folder}")
        self.download_folder = download_folder
        self.logger = logger
        os.makedirs(download_folder, exist_ok=True)

    def download_video(self, url) -> str:
        """
        Downloads the best audio stream from a YouTube video.

        Args:
            url: YouTube video URL

        Returns:
            Path to the downloaded audio file (e.g., .m4a)

        Raises:
            RuntimeError if the download fails
        """
        self.logger.logStartAction(f"Download YouTube Audio: {url}")

        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(self.download_folder, 'yt_%(id)s.%(ext)s'),
                'quiet': False,
                'noplaylist': True,
                'merge_output_format': 'm4a',
                'postprocessors': [
                    {
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'm4a',
                        'preferredquality': '192',
                    }
                ]
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                base = ydl.prepare_filename(info)
                audio_path = os.path.splitext(base)[0] + ".m4a"

            self.logger.logEndAction(f"Download YouTube Audio: {url}")
            return audio_path

        except Exception as e:
            self.logger.addLog(f"❌ Failed to download YouTube audio: {url} | Error: {e}")
            raise RuntimeError(f"Failed to download YouTube audio: {e}")