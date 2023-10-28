import sys
import subprocess
import openai
import os

# Load OpenAI API key from properties file
with open('openai-key.properties', 'r') as file:
    api_key = file.read().strip()

# Set up OpenAI API client
openai.api_key = api_key

# Get audio file name from command line arguments
audio_file = sys.argv[1]

# Convert MP3 to WAV for more predictable file size
def convert_mp3_to_wav(filename):
    wav_filename = filename.replace('.mp3', '.wav')
    command = ['ffmpeg', '-i', filename, wav_filename]
    subprocess.run(command)
    return wav_filename

# Split the WAV audio file into chunks of approximate size
def split_audio(filename, chunk_size):
    # Get the size per second of the audio file
    file_size = os.path.getsize(filename)
    duration_command = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', filename]
    duration_output = subprocess.check_output(duration_command).decode('utf-8').strip()
    duration = float(duration_output)
    size_per_second = file_size / duration
    
    # Calculate the duration for each chunk
    chunk_duration = chunk_size / size_per_second
    
    # Split the audio file into chunks
    command = [
        'ffmpeg',
        '-i', filename,
        '-f', 'segment',
        '-segment_time', str(chunk_duration),
        '-c', 'copy',
        'chunk-%03d.wav'
    ]
    subprocess.run(command)

# Convert the WAV chunks back to MP3
def convert_chunks_to_mp3():
    for i in range(999):  # Assumes there are fewer than 1000 chunks
        wav_chunk_file = f'chunk-{i:03d}.wav'
        mp3_chunk_file = wav_chunk_file.replace('.wav', '.mp3')
        try:
            command = ['ffmpeg', '-i', wav_chunk_file, mp3_chunk_file]
            subprocess.run(command)
        except FileNotFoundError:
            break  # Stop when no more chunks are found

# Transcribe each MP3 chunk
def transcribe_chunks():
    for i in range(999):  # Assumes there are fewer than 1000 chunks
        mp3_chunk_file = f'chunk-{i:03d}.mp3'
        try:
            with open(mp3_chunk_file, 'rb') as file:
                response = openai.Speech.create(
                    file=file,
                    format="mp3"
                )
                print(f'Chunk {i}: {response["choices"][0]["text"]}')
        except FileNotFoundError:
            break  # Stop when no more chunks are found

# Convert MP3 to WAV
wav_file = convert_mp3_to_wav(audio_file)

# Define desired chunk size in bytes (e.g., 20MB)
desired_chunk_size = 20 * 1024 * 1024

# Split the WAV audio file
split_audio(wav_file, desired_chunk_size)

# Convert WAV chunks back to MP3
convert_chunks_to_mp3()

# Transcribe MP3 chunks
transcribe_chunks()
