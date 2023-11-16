import ffmpeg
import os

class VideoProcessor:
    def __init__(self, video_path):
        self.video_path = video_path

    def extract_audio(self, output_format='mp3'):
        if not os.path.exists(self.video_path):
            raise FileNotFoundError(f"Video file not found: {self.video_path}")

        output_audio_path = self.video_path.rsplit('.', 1)[0] + f".{output_format}"

        try:
            (
                ffmpeg
                .input(self.video_path)
                .output(output_audio_path, format=output_format)
                .run(overwrite_output=True, quiet=True)
            )
            return output_audio_path
        except ffmpeg.Error as e:
            print(f"ffmpeg error: {e.stderr}")
            return None
        except Exception as e:
            print(f"An error occurred during audio extraction: {e}")
            return None