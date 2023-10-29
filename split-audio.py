from pydub import AudioSegment
import math
import sys
import os

class SplitWavAudioMubin():
    def __init__(self, folder, filename):
        self.folder = folder
        self.filename = filename
        self.filepath = folder + '/' + filename
        
        self.audio = AudioSegment.from_mp3(self.filepath)
    
    def get_duration(self):
        return self.audio.duration_seconds
    
    def single_split(self, from_min, to_min, split_filename):
        t1 = from_min * 60 * 1000
        t2 = to_min * 60 * 1000
        split_audio = self.audio[t1:t2]
        split_audio.export(self.folder + '/' + split_filename, format="mp3")
        
    def multiple_split(self, min_per_split):
        total_mins = math.ceil(self.get_duration() / 60)
        for i in range(0, total_mins, min_per_split):
            split_fn = str(i) + '_' + self.filename
            self.single_split(i, i+min_per_split, split_fn)
            print(str(i) + ' Done')
            if i == total_mins - min_per_split:
                print('All splited successfully')


# Get the input file path from the command-line arguments
input_file_path = sys.argv[1]
print(input_file_path)
input_folder = os.path.dirname(input_file_path)
input_filename = os.path.basename(input_file_path)

audio_splitter = SplitWavAudioMubin(folder=input_folder, filename=input_filename)
# Split the entire audio into chunks of 5 minutes each
audio_splitter.multiple_split(min_per_split=20)

