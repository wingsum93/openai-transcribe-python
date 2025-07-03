from .logger import Logger
import ffmpeg
import os

class VideoProcessor:
    def __init__(self, download_folder="downloads",logger:Logger = Logger()):
        self.download_folder = download_folder
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)
        self.logger = logger

    def convert_video_to_audio(self, video_path:str, audio_format="mp3"):
        print(f"VideoProcessor  video: {video_path}, format {audio_format}")
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

        # 提取文件名（不包括扩展名）
        file_name = os.path.basename(video_path).split('.')[0]
        audio_path = os.path.join(self.download_folder, file_name + f'.{audio_format}')
        print(f"VideoProcessor audio path: {audio_path},  vi: {video_path}")

        # Skip if audio already converted
        if os.path.exists(audio_path):
            print(f"VideoProcessor audio already converted: {audio_path}")
            return audio_path
        self.logger.logStartAction('convert_video_to_audio')
        try:
            (
                ffmpeg
                .input(video_path)
                .output(audio_path, acodec='copy', vn=None)
                .run(overwrite_output=True)
            )
            self.logger.logEndAction('convert_video_to_audio')
            return audio_path
        except ffmpeg.Error as e:
            print(f"An error occurred during video-to-audio conversion: {e.stderr}")
            return None
