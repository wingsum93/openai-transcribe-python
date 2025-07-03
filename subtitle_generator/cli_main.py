import click
from subtitle_generator.processor import run_transcription
from util.search import list_files_with_extension
from util.count_file_number import list_video_files_recursive

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
