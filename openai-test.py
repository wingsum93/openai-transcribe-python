from pydub import AudioSegment
import openai
import sys

def transcribe_large_audio(file_path):
    # Load the audio file
    audio = AudioSegment.from_mp3(file_path)

    # Split the audio file into chunks of 30 seconds
    chunk_length = 10 * 60 * 1000  # 30 seconds in milliseconds
    chunks = [audio[i:i+chunk_length] for i in range(0, len(audio), chunk_length)]

    # Load API key from properties file
    with open("openai-key.properties", "r") as file:
        api_key = file.read().strip()

    # Set the API key for OpenAI
    openai.api_key = api_key

    # Initialize an empty string to hold the full transcript
    full_transcript = ""

    # Transcribe each chunk
    for i, chunk in enumerate(chunks):
        # Save the chunk to a temporary file
        chunk.export(f"chunk{i}.mp3", format="mp3")

        # Open the chunk file
        with open(f"chunk{i}.mp3", "rb") as audio_file:
            # Transcribe the audio chunk
            response = openai.Audio.transcribe("whisper-1", audio_file)

            # Append the transcript to the full transcript
            full_transcript += response['text'] + "\n"
            print("processed {i} file")

    # Save the full transcript to the output file
    with open("output_text.txt", "w") as file:
        file.write(full_transcript)

# Get the input file path from the command-line arguments
input_file_path = sys.argv[1]

# Call the function to transcribe the audio file
transcribe_large_audio(input_file_path)
