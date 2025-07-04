import click
from subtitle_generator.processor import run_transcription
from subtitle_generator.util.search import list_files_with_extension
from subtitle_generator.util.count_file_number import list_video_files_recursive
from subtitle_generator.youtube_processor import YoutubeProcessor
from subtitle_generator.video_processor import VideoProcessor
from subtitle_generator.facebook_processor import FacebookProcessor
from subtitle_generator.recorder import record_until_end
import datetime
import os

@click.group()
def cli():
    """OpenAI Whisper Subtitle Generator CLI"""
    pass

@cli.group()
def transcribe():
    """Transcribe a single file (local, YouTube, Facebook)"""
    pass

@transcribe.command("local")
@click.option("--file", required=True, help="Path to local video or audio file")
@click.option("--source", "-sl", required=True, type=click.Choice(["zh", "en", "ja", "Auto"]), help="Source language")
@click.option("--target", "-tl", type=click.Choice(["zh", "en", "ja"]), help="Target translation language")
@click.option("--model", "-m", default="small", type=click.Choice(["tiny","base","small","medium","medium.en","large","large-v2","large-v3"]), help="Whisper model type")
@click.option("--srt", is_flag=True, help="Generate .srt subtitle")
@click.option("--vtt", is_flag=True, help="Generate .vtt subtitle")
@click.option("--txt", is_flag=True, help="Generate .txt transcription")
@click.option("--output-dir", default="output", help="Directory to save subtitle files")
def transcribe_local(file, source, target, model, srt, vtt, txt, output_dir):
    """Transcribe local video/audio file"""
    config = {
        "video_path": file,
        "source_language": source,
        "target_language": target,
        "model_type": model,
        "enable_txt": txt,
        "enable_srt": srt,
        "enable_vtt": vtt,
        "output_dir": output_dir,
        "keep_origin_subtitle": True,
    }

    run_transcription("local", config)

@cli.command("transcribe-many")
@click.option("--file", required=True, type=click.Path(exists=True), help="Path to a .txt file with video/audio paths (one per line)")
@click.option("--source", "-sl", required=True, type=click.Choice(["zh", "en", "ja", "Auto"]))
@click.option("--target", "-tl", type=click.Choice(["zh", "en", "ja"]))
@click.option("--model", "-m", default="small", type=click.Choice([
    "tiny", "base", "small", "medium", "medium.en", "large", "large-v2", "large-v3"
]))
@click.option("--srt", is_flag=True)
@click.option("--vtt", is_flag=True)
@click.option("--txt", is_flag=True)
@click.option("--output-dir", default="output")
@click.option("--no-skip", is_flag=True, help="Do not skip files with existing outputs")
def transcribe_many(file, source, target, model, srt, vtt, txt, output_dir, no_skip):
    """Transcribe multiple local video/audio files"""

    config = {
        "source_language": source,
        "target_language": target,
        "model_type": model,
        "enable_txt": txt,
        "enable_srt": srt,
        "enable_vtt": vtt,
        "output_dir": output_dir,
        "keep_origin_subtitle": True,
    }

    run_transcription_batch("local", file, config, skip_existing=not no_skip)

@transcribe.command("youtube")
@click.option("--url", required=True, help="YouTube video URL")
@click.option("--source", "-sl", required=True, type=click.Choice(["zh", "en", "ja", "Auto"]), help="Source language")
@click.option("--target", "-tl", type=click.Choice(["zh", "en", "ja"]), help="Target translation language")
@click.option("--model", "-m", default="small", type=click.Choice(["tiny","base","small","medium","medium.en","large","large-v2","large-v3"]), help="Whisper model type")
@click.option("--srt", is_flag=True, help="Generate .srt subtitle")
@click.option("--vtt", is_flag=True, help="Generate .vtt subtitle")
@click.option("--txt", is_flag=True, help="Generate .txt transcription")
@click.option("--output-dir", default="output", help="Directory to save subtitle files")
def transcribe_youtube(url, source, target, model, srt, vtt, txt, output_dir):
    """Transcribe audio from a YouTube URL"""
    
    config = {
        "video_path": url,
        "source_language": source,
        "target_language": target,
        "model_type": model,
        "enable_txt": txt,
        "enable_srt": srt,
        "enable_vtt": vtt,
        "output_dir": output_dir,
        "keep_origin_subtitle": True,
    }
    run_transcription("youtube", config)


@cli.command("transcribe-batch-youtube")
@click.option("--file", required=True, type=click.Path(exists=True))
@click.option("--source", "-sl", required=True, type=click.Choice(["zh", "en", "ja", "Auto"]))
@click.option("--target", "-tl", type=click.Choice(["zh", "en", "ja"]))
@click.option("--model", "-m", default="small", type=click.Choice(["tiny","base","small","medium","medium.en","large","large-v2","large-v3"]), help="Whisper model type")
@click.option("--srt", is_flag=True)
@click.option("--vtt", is_flag=True)
@click.option("--txt", is_flag=True)
@click.option("--output-dir", default="output")
@click.option("--no-skip", is_flag=True, help="Do not skip existing files")
def transcribe_batch_youtube(file, source, target, model, srt, vtt, txt, output_dir, no_skip):
    if not os.path.exists(file):
        raise FileNotFoundError(f"Input list file does not exist: {file}")

    with open(file, "r", encoding="utf-8") as f:
        entries = [line.strip() for line in f if line.strip()]

    shared_config = {
        "source_language": source,
        "target_language": target,
        "model_type": model,
        "enable_txt": txt,
        "enable_srt": srt,
        "enable_vtt": vtt,
        "output_dir": output_dir,
        "keep_origin_subtitle": True,
    }
    run_transcription_batch(
        source_type="youtube",
        list_file_path=file,
        shared_config=shared_config,
        skip_existing=not no_skip,
    )
          
@transcribe.command("facebook")
@click.option("--url", required=True, help="Facebook video URL (public)")
@click.option("--source", "-sl", required=True, type=click.Choice(["zh", "en", "ja", "Auto"]), help="Source language")
@click.option("--target", "-tl", type=click.Choice(["zh", "en", "ja"]), help="Target translation language")
@click.option("--model", "-m", default="small", type=click.Choice([
    "tiny", "base", "small", "medium", "medium.en", "large", "large-v2", "large-v3"
]), help="Whisper model type")
@click.option("--srt", is_flag=True, help="Generate .srt subtitle")
@click.option("--vtt", is_flag=True, help="Generate .vtt subtitle")
@click.option("--txt", is_flag=True, help="Generate .txt transcription")
@click.option("--output-dir", default="output", help="Directory to save subtitle files")
@click.option("--no-skip", is_flag=True, help="Do not skip if files already exist")
def transcribe_facebook(url, source, target, model, srt, vtt, txt, output_dir, no_skip):
    """Transcribe a Facebook video to subtitles"""
    # Download the Facebook video
    fb = FacebookProcessor()
    try:
        video_path = fb.download_video(url)
    except Exception as e:
        print(f"❌ Error downloading Facebook video: {e}")
        return

    # Prepare config
    config = {
        "video_path": video_path,
        "source_language": source,
        "target_language": target,
        "model_type": model,
        "enable_txt": txt,
        "enable_srt": srt,
        "enable_vtt": vtt,
        "output_dir": output_dir,
        "keep_origin_subtitle": True,
    }

    try:
        run_transcription("local", config)
    except Exception as e:
        print(f"❌ Failed to transcribe: {e}")

@cli.command("record")
@click.option("--source", "-sl", required=True, type=click.Choice(["zh", "en", "ja", "Auto"]))
@click.option("--target", "-tl", type=click.Choice(["zh", "en", "ja"]))
@click.option("--model", "-m", default="small", type=click.Choice([
    "tiny", "base", "small", "medium", "medium.en", "large", "large-v2", "large-v3"
]))
@click.option("--srt", is_flag=True)
@click.option("--vtt", is_flag=True)
@click.option("--txt", is_flag=True)
@click.option("--output-dir", default="output")
def record(source, target, model, srt, vtt, txt, output_dir):
    """🎤 錄音直到輸入 'end'，並轉錄成字幕 / 文字檔"""
    
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    audio_path = os.path.join("recordings", f"recording_{now}.wav")
    record_until_end(audio_path)

    config = {
        "video_path": audio_path,
        "source_language": source,
        "target_language": target,
        "model_type": model,
        "enable_txt": txt,
        "enable_srt": srt,
        "enable_vtt": vtt,
        "output_dir": output_dir,
        "keep_origin_subtitle": True,
    }

    run_transcription("local", config)
            
def run_transcription_batch(
    source_type: str,
    list_file_path: str,
    shared_config: dict,
    skip_existing: bool = True,
):
    """
    Process a batch of video/audio sources listed in a file.

    Args:
        source_type: "youtube" or "local"
        list_file_path: path to the .txt file containing URLs or file paths (one per line)
        shared_config: common config for all items, e.g.:
            {
                "source_language": "zh",
                "target_language": "en",
                "model_type": "medium",
                "output_dir": "output",
                "enable_txt": True,
                "enable_srt": True,
                "enable_vtt": False,
                "keep_origin_subtitle": True
            }
        skip_existing: if True, skip transcription if output files already exist
    """
    if not os.path.exists(list_file_path):
        raise FileNotFoundError(f"Input list file does not exist: {list_file_path}")

    with open(list_file_path, "r", encoding="utf-8") as f:
        entries = [line.strip() for line in f if line.strip()]

    for idx, entry in enumerate(entries):
        print(f"\n▶️ [{idx+1}/{len(entries)}] Processing: {entry}")

        try:
            # Determine output base name
            base_name = os.path.splitext(os.path.basename(entry))[0]
            suffix = shared_config.get("target_language") or shared_config["source_language"]
            output_dir = shared_config.get("output_dir", "output")

            expected_outputs = []
            if shared_config.get("enable_txt"):
                expected_outputs.append(f"{base_name}-{suffix}.txt")
            if shared_config.get("enable_srt"):
                expected_outputs.append(f"{base_name}-{suffix}.srt")
            if shared_config.get("enable_vtt"):
                expected_outputs.append(f"{base_name}-{suffix}.vtt")

            outputs_exist = all(os.path.exists(os.path.join(output_dir, fname)) for fname in expected_outputs)

            if skip_existing and outputs_exist:
                print(f"✅ Skipping (already done): {base_name}")
                continue

            config = {
                **shared_config,
                "video_path": entry
            }

            run_transcription(source_type, config)

        except Exception as e:
            print(f"❌ Error processing {entry}: {e}")
@cli.group()
def utils():
    """Utility tools"""
    pass

@utils.command("search")
@click.argument("folder", type=click.Path(exists=True))
@click.argument("ext")
def search(folder, ext):
    """Search files by extension and write to result.txt"""
    list_files_with_extension(folder, ext, "result.txt")

@utils.command("count")
@click.argument("folder", type=click.Path(exists=True))
def count(folder):
    """Count all video files in folder"""
    videos = list(list_video_files_recursive(folder))
    click.echo(f"Found {len(videos)} video files:")
    for f in videos:
        click.echo(f)

if __name__ == "__main__":
    cli()
