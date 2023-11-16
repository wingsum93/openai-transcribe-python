
import argparse
from transcribe_video import VideoRecognizer
from youtube_processor import YoutubeProcessor

def main(config):
    vr1 = VideoRecognizer(video_path=config['video_path'], source_language=config['source_language'], target_language=config['target_language'], output_filename=config['output_filename'], output_dir=config['output_dir'], model_type=config['model_type'])
    if config['enable_txt']:
        vr1.add_text_output()
    if config['enable_srt']:
        vr1.add_srt_output()
    if config['enable_vtt']:
        vr1.add_vtt_output()
    vr1.detectVideo()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Transcribe a video using OpenAI Whisper.')
    parser.add_argument('--video_path', type=str, required=True, help='The path to the video file or a YouTube URL.')
    parser.add_argument('--model_type', type=str, choices=['tiny','base', 'small', 'medium', 'large','large-v2','large-v3'], default='small', help='The type of Whisper model to use.')
    parser.add_argument('-sl','--source_language', type=str, choices=['zh', 'en', 'ja'], required=True, help='The type of language that video use.')
    parser.add_argument('-tl','--target_language', type=str, choices=['zh', 'en', 'ja'], help='Language of video want to translate.')
    parser.add_argument('--output_dir', type=str, help='The directory of output file')
    parser.add_argument('--output_filename', type=str, help='The filename of subtitle file')

    parser.add_argument('-et','--enable_txt', action='store_false', help='Output Text file')
    parser.add_argument('-es','--enable_srt', action='store_true', help='Output SRT file')
    parser.add_argument('-ev','--enable_vtt', action='store_true', help='Output VTT file')

    args = parser.parse_args()
    config = {
        'video_path': args.video_path,
        'model_type': args.model_type,
        'source_language': args.source_language,
        'target_language': args.target_language,
        'output_dir': args.output_dir,
        'output_filename': args.output_filename,
        'enable_txt': args.enable_txt,
        'enable_srt': args.enable_srt,
        'enable_vtt': args.enable_vtt
    }

    main(config)
    
    