import whisper
import torch
import gc

@contextmanager
def use_whisper_model(model_type,device):
    model = whisper.load_model(model_type, device=device)
    try:
        yield model
    finally:
        del model
        gc.collect()

class SubtitleGenerator:
    def __init__(self, audio_file_path,source_language):
        self.audio_file_path = audio_file_path
        self.source_language = source_language
        # Ensure a GPU is available
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
    def generate_subtitles(self):
        # This function should handle the process of generating subtitles.
        # For the sake of this example, it's a placeholder function.
        # In a real-world scenario, you would integrate with a speech-to-text service here.

        subtitles = self.transcribe_audio_to_text(self.audio_file_path)
        return subtitles

    @staticmethod
    def transcribe_audio_to_segment(audio_path):
        
        with use_whisper_model(self.model_type,self.device) as whisper_model:
            options = whisper.DecodingOptions(fp16=False, language=self.source_language)
            result = whisper_model.transcribe(audio_path, **options.__dict__, verbose=False)
        # Mocked return value for the sake of example.
        return result

    # You can add more methods here for additional functionalities,
    # like formatting the subtitles, handling different languages, etc.
