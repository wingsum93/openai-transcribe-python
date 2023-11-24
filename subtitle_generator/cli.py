
import argparse
from youtube_processor import YoutubeProcessor
from subtitle_generator import SubtitleGenerator
from video_processor import VideoProcessor


ACTION_PROCESS_VIDEO = 'process-video'
ACTION_PROCESS_MP3 = 'process-mp3'
ACTION_PROCESS_YOUTUBE = 'process-youtube'

def main(config):
    video_path = config['video_path']
    print(f"v path: {video_path}")
    # Check if the video path is a YouTube URL and download the video
    
    youtube_processor = YoutubeProcessor()
    video = youtube_processor.download_video(url=video_path)


    # Video convert to audio
    vp = VideoProcessor()
    audio_path = vp.convert_video_to_audio(video,"aac")
    # Subtitle generation
    subtitle_generator = SubtitleGenerator(audio_file_path= audio_path,
                                           source_language=config['source_language'],
                                           target_language=config['target_language'], 
                                           output_dir=config['output_dir'],
                                           model_type=config['model_type'])
    if config['enable_txt']:
        subtitle_generator.add_text_output()
    if config['enable_srt']:
        subtitle_generator.add_srt_output()
    if config['enable_vtt']:
        subtitle_generator.add_vtt_output()
    subtitles = subtitle_generator.generate_subtitles()


    
    
    
def process_local_audio(config):
    # Subtitle generation
    subtitle_generator = SubtitleGenerator(audio_file_path= config['video_path'],
                                           source_language=config['source_language'],
                                           target_language=config['target_language'], 
                                           output_dir=config['output_dir'],
                                           model_type=config['model_type'])
    if config['enable_txt']:
        subtitle_generator.add_text_output()
    if config['enable_srt']:
        subtitle_generator.add_srt_output()
    if config['enable_vtt']:
        subtitle_generator.add_vtt_output()
    subtitles = subtitle_generator.generate_subtitles()

def process_local_video(config):
    # Video convert to audio
    vp = VideoProcessor()
    audio_path = vp.convert_video_to_audio(config['video_path'],"aac")
    # Subtitle generation
    subtitle_generator = SubtitleGenerator(audio_file_path= audio_path,
                                           source_language=config['source_language'],
                                           target_language=config['target_language'], 
                                           output_dir=config['output_dir'],
                                           model_type=config['model_type'])
    if config['enable_txt']:
        subtitle_generator.add_text_output()
    if config['enable_srt']:
        subtitle_generator.add_srt_output()
    if config['enable_vtt']:
        subtitle_generator.add_vtt_output()
    subtitles = subtitle_generator.generate_subtitles()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Transcribe a video using OpenAI Whisper.')
    # action
    parser.add_argument('action', type=str, choices=[ACTION_PROCESS_VIDEO,ACTION_PROCESS_MP3,ACTION_PROCESS_YOUTUBE], help='The path to the video file or a YouTube URL.')

    parser.add_argument('video_path', type=str, help='The path to the video file or a YouTube URL.')

    # all non positional args
    parser.add_argument('-m','--model', type=str, choices=['tiny','base', 'small', 'medium', 'large','large-v2','large-v3'], default='small', help='The type of Whisper model to use.')
    parser.add_argument('-sl','--source_language', type=str, choices=['zh', 'en', 'ja'], required=True, help='The type of language that video use.')
    parser.add_argument('-tl','--target_language', type=str, choices=['zh', 'en', 'ja'], help='Language of video want to translate.')
    parser.add_argument('-od','--output_dir', type=str, help='The directory of output file')
    parser.add_argument('-ofn','--output_filename', type=str, help='The filename of subtitle file')

    parser.add_argument('-et','--enable_txt', action='store_false', help='Output Text file')
    parser.add_argument('-es','--enable_srt', action='store_true', help='Output SRT file')
    parser.add_argument('-ev','--enable_vtt', action='store_true', help='Output VTT file')

    args = parser.parse_args()
    config = {
        'video_path': args.video_path,
        'model_type': args.model,
        'source_language': args.source_language,
        'target_language': args.target_language,
        'output_dir': args.output_dir,
        'output_filename': args.output_filename,
        'enable_txt': args.enable_txt,
        'enable_srt': args.enable_srt,
        'enable_vtt': args.enable_vtt
    }

    if args.action == ACTION_PROCESS_YOUTUBE:
        main(config)
    elif args.action == ACTION_PROCESS_MP3:
        process_local_audio(config)
    elif args.action == ACTION_PROCESS_VIDEO:
        process_local_video(config)
    
    