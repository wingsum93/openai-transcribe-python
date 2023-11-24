import ffmpeg
import os

class VideoProcessor:
    def __init__(self, download_folder="downloads"):
        self.download_folder = download_folder
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

    def convert_video_to_audio(self, video_path:str, audio_format="mp3"):
        print(f"VideoProcessor  video: {video_path}, format {audio_format}")
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

        audio_path = os.path.splitext(video_path)[0] + f".{audio_format}"
        print(f"VideoProcessor audio path: {audio_path},  vi: {video_path}")
        try:
            (
                ffmpeg
                .input(video_path)
                .output(audio_path, acodec='copy', vn=None)
                .run(overwrite_output=True)
            )
            return audio_path
        except ffmpeg.Error as e:
            print(f"An error occurred during video-to-audio conversion: {e.stderr}")
            return None
