import argparse
from pytube import YouTube


def main(video_url):
    yt = YouTube(video_url)
    # Select the highest resolution stream available
    stream = yt.streams.get_highest_resolution()
    try:
        stream.download()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Transcribe a video using OpenAI Whisper.')
    parser.add_argument('--video_url', type=str, required=True, help='The path to the video file or a YouTube URL.')
    args = parser.parse_args()

    main(args.video_url)