from subtitle_generator import VideoProcessor, SubtitleGenerator

def run_transcription(source_type, config):
    if source_type == "local":
        vp = VideoProcessor()
        audio_path = vp.convert_video_to_audio(config["video_path"], "aac")

        subtitle_generator = SubtitleGenerator(
            audio_file_path=audio_path,
            source_language=config["source_language"],
            target_language=config["target_language"],
            output_dir=config["output_dir"],
            keep_origin_subtitle=config["keep_origin_subtitle"],
            model_type=config["model_type"]
        )
        if config["enable_txt"]:
            subtitle_generator.add_text_output()
        if config["enable_srt"]:
            subtitle_generator.add_srt_output()
        if config["enable_vtt"]:
            subtitle_generator.add_vtt_output()

        subtitle_generator.generate_subtitles()
