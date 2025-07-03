import os
import sys

def list_video_files_recursive(folder):
    """
    List all video files in a folder, including files in subfolders recursively.
    Filters based on common video file extensions.
    """
    video_extensions = {'.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv'}
    for root, dirs, files in os.walk(folder):
        for file in files:
            if os.path.splitext(file)[1].lower() in video_extensions:
                yield os.path.join(root, file)

# Example usage
folder_path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()  # Use current directory if no argument provided
video_files = list(list_video_files_recursive(folder_path))
size = len(video_files)
print(f"Number of video files: {size}")
for file in video_files:
    print(file)
