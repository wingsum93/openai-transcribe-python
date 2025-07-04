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
        print(f"🎞️ 轉換影片或音訊檔案： {video_path}")
        
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"搵唔到檔案： {video_path}")

        # ✅ Already supported by Whisper? No conversion needed
        supported_exts = [".aac", ".m4a", ".wav"]
        if any(video_path.lower().endswith(ext) for ext in supported_exts):
            print(f"✅ 檔案格式支援（{os.path.splitext(video_path)[1]}），毋須轉換")
            return video_path

        # Extract name and prepare output
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        audio_path = os.path.join(self.download_folder, f"{base_name}.{audio_format}")

        if os.path.exists(audio_path):
            print(f"✅ 已轉換過：{audio_path}")
            return audio_path

        self.logger.logStartAction("轉換音訊")
        try:
            acodec = "aac" if audio_format == "aac" else "pcm_s16le"

            (
                ffmpeg
                .input(video_path)
                .output(audio_path, acodec=acodec, vn=None)
                .run(overwrite_output=True)
            )

            self.logger.logEndAction("轉換音訊")
            return audio_path

        except ffmpeg.Error as e:
            raise ValueError(f"❌ 轉換失敗：{e.stderr.decode()}") from e
