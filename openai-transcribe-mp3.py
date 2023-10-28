import openai
import soundfile as sf
import os
import sys
import configparser

# Function to split audio file into chunks less than 25MB
def split_audio(file_path, chunk_size=24000000):  # chunk_size in bytes
    data, samplerate = sf.read(file_path)
    total_bytes = data.nbytes
    num_chunks = total_bytes // chunk_size + (1 if total_bytes % chunk_size > 0 else 0)
    sf.write(file_path.replace('.wav', '_chunk0.wav'), data[:chunk_size//2], samplerate)
    for i in range(1, num_chunks):
        start_idx = i * chunk_size//2
        end_idx = (i + 1) * chunk_size//2
        sf.write(file_path.replace('.wav', f'_chunk{i}.wav'), data[start_idx:end_idx], samplerate)

# Function to transcribe audio chunks
def transcribe_chunks(file_path):
    split_audio(file_path)
    transcripts = []
    for i in range(10):  # Assuming a maximum of 10 chunks to simplify
        chunk_path = file_path.replace('.wav', f'_chunk{i}.wav')
        try:
            with open(chunk_path, 'rb') as audio_file:
                response = openai.Audio.create(
                    engine="davinci",
                    file=audio_file,
                    mime_type="audio/wav"
                )
                transcripts.append(response['choices'][0]['text'])
        except FileNotFoundError:
            break  # No more chunks
    full_transcript = ' '.join(transcripts)
    
    # Writing the transcript to a text file
    txt_file_path = os.path.splitext(file_path)[0] + '.txt'
    with open(txt_file_path, 'w') as txt_file:
        txt_file.write(full_transcript)
    
    return txt_file_path  # Returning the path of the text file

if __name__ == "__main__":
    # Load API key from properties file
    config = configparser.ConfigParser()
    config.read('openai-key.properties')
    openai.api_key = config['Credentials']['API_KEY']
    
    if len(sys.argv) != 2:
        print("Usage: python script.py <audio-file-path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    txt_file_path = transcribe_chunks(file_path)
    print(f'Transcript saved to: {txt_file_path}')
