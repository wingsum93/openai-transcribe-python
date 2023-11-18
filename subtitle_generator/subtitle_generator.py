from contextlib import contextmanager
import whisper
import torch
import gc

@contextmanager
def use_whisper_model(model_type, device):
    model = whisper.load_model(model_type, device=device)
    try:
        yield model
    finally:
        del model
        if device == 'cuda':
            torch.cuda.empty_cache()  # Clear memory cache if the device is CUDA
        gc.collect()

class SubtitleGenerator:
    def __init__(self, audio_file_path, source_language, model_type):
        self.audio_file_path = audio_file_path
        self.source_language = source_language
        self.model_type = model_type  # Add model_type as an instance attribute
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

    def generate_subtitles(self):
        # This function should handle the process of generating subtitles.
        # Placeholder function for this example.
        subtitles = self.transcribe_audio_to_segment(self.audio_file_path)
        return subtitles

    def transcribe_audio_to_segment(self, audio_path):
        # Now an instance method, not a static method
        with use_whisper_model(self.model_type, self.device) as whisper_model:
            options = whisper.DecodingOptions(fp16=False, language=self.source_language)
            result = whisper_model.transcribe(audio_path, **options.__dict__, verbose=False)
        return result

    # Additional methods can be added here.
