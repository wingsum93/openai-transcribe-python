from .logger import Logger
import ffmpeg
import os

class VideoProcessor:
    def __init__(self, download_folder="downloads",logger:Logger = Logger()):
        self.download_folder = download_folder
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)
        self.logger = logger

    def convert_video_to_audio(self, video_path:str, audio_format="aac")-> str:
        print(f"VideoProcessor  video: {video_path}, format {audio_format}")
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

        # ✅ Skip conversion if already desired format
        if video_path.endswith(f".{audio_format}"):
            print(f"Input is already in desired audio format: {video_path}")
            return video_path
        # 提取文件名（不包括扩展名）
        file_name = os.path.splitext(os.path.basename(video_path))[0]
        audio_path = os.path.join(self.download_folder, f"{file_name}.{audio_format}")
        print(f"VideoProcessor audio path: {audio_path},  vi: {video_path}")

        # Skip if audio already converted
        if os.path.exists(audio_path):
            print(f"VideoProcessor audio already converted: {audio_path}")
            return audio_path
        self.logger.logStartAction('convert_video_to_audio')
        try:
            if audio_format not in ['aac', 'wav']:
                raise ValueError("Unsupported audio format. Supported formats: aac, mp3, wav")
            acodec = 'aac' if audio_format == 'aac' else 'pcm_s16le'

            (
                ffmpeg
                .input(video_path)
                .output(audio_path, acodec=acodec, vn=None)
                .run(overwrite_output=True)
            )
            self.logger.logEndAction('convert_video_to_audio')
            return audio_path
        except ffmpeg.Error as e:
            raise ValueError(f"Error converting video to audio: {e.stderr.decode()}") from e
