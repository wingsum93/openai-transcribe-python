import os
import yt_dlp
from subtitle_generator.logger import Logger

class FacebookProcessor:
    def __init__(self, download_folder="downloads", logger=Logger()):
        self.download_folder = download_folder
        self.logger = logger
        os.makedirs(self.download_folder, exist_ok=True)

    def download_video(self, url: str) -> str:
        """
        Downloads the best available audio from a Facebook video using yt-dlp.

        Returns:
            The path to the downloaded audio file (e.g., .m4a or .webm)
        """
        self.logger.logStartAction(f"Download Facebook Audio: {url}")

        try:
            ydl_opts = {
                'outtmpl': os.path.join(self.download_folder, 'fb_%(id)s.%(ext)s'),
                'format': 'bestaudio/best',
                'quiet': False,
                'noplaylist': True,
                'merge_output_format': 'm4a',  # fallback
                'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'm4a',
                    'preferredquality': '192',
                }
            ]
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info_dict)
                audio_path = os.path.splitext(filename)[0] + ".m4a"

            self.logger.logEndAction(f"Download Facebook Audio: {url}")
            return audio_path

        except Exception as e:
            self.logger.addLog(f"❌ Failed to download Facebook audio: {url} | Error: {e}")
            raise RuntimeError(f"Failed to download Facebook audio: {e}")
