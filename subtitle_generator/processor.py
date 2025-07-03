from subtitle_generator.video_processor import VideoProcessor
from subtitle_generator.subtitle_generator import SubtitleGenerator
from subtitle_generator.youtube_processor import YoutubeProcessor

def run_transcription(source_type: str, config: dict):
    """
    Runs the transcription pipeline.

    Args:
        source_type: One of ["local", "youtube"]
        config: {
            video_path: str,
            source_language: str,
            target_language: str,
            model_type: str,
            output_dir: str,
            keep_origin_subtitle: bool,
            enable_txt: bool,
            enable_srt: bool,
            enable_vtt: bool
        }
    Returns:
        Path to generated subtitles
    """
    # Step 1: Determine audio source
    if source_type == "youtube":
        yt = YoutubeProcessor()
        video_path = yt.download_video(config["video_path"])
    elif source_type == "local":
        video_path = config["video_path"]
    else:
        raise ValueError(f"Unsupported source_type: {source_type}")

    # Step 2: Convert to audio
    vp = VideoProcessor()
    audio_path = vp.convert_video_to_audio(video_path, "aac")

    # Step 3: Transcribe + Translate
    sg = SubtitleGenerator(
        audio_file_path=audio_path,
        source_language=config["source_language"],
        target_language=config["target_language"],
        output_dir=config["output_dir"],
        model_type=config["model_type"],
        keep_origin_subtitle=config.get("keep_origin_subtitle", True),
    )
    if config.get("enable_txt"): sg.add_text_output()
    if config.get("enable_srt"): sg.add_srt_output()
    if config.get("enable_vtt"): sg.add_vtt_output()

    segments = sg.generate_subtitles()
    return segments