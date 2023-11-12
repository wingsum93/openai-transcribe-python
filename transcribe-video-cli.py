
import argparse
from transcribe_video import VideoRecognizer

def main(config):
    vr1 = VideoRecognizer(video_path=config['video_path'], language=config['language'], model_type=config['model_type'])

    vr1.detectVideo()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Transcribe a video using OpenAI Whisper.')
    parser.add_argument('--video_path', type=str, required=True, help='The path to the video file or a YouTube URL.')
    parser.add_argument('--model_type', type=str, choices=['tiny','base', 'small', 'medium', 'large','large-v2','large-v3'], default='small', help='The type of Whisper model to use.')
    parser.add_argument('--lang', type=str, choices=['zh', 'en', 'ja'], required=True, help='The type of language that video use.')

    parser.add_argument('--enable_txt', action='store_false', help='Output Text file')
    parser.add_argument('--enable_srt', action='store_true', help='Output SRT file')
    parser.add_argument('--enable_vtt', action='store_true', help='Output VTT file')

    args = parser.parse_args()
    config = {
        'video_path': args.video_path,
        'model_type': args.model_type,
        'language': args.lang,
        'enable_txt': args.enable_txt,
        'enable_srt': args.enable_srt,
        'enable_vtt': args.enable_vtt
    }
    main(config)
    
    