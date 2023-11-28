from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
from logger import Logger

class TextTranslator:
    def __init__(self,logger=Logger(), model_name="facebook/m2m100_418M"):
        self.logger = logger
        self.model_name = model_name
        self.translation_cache = {}  # Initialize an empty cache

    # Translate multiple text lines
    def translate(self, segments, source_language, target_language):
        self.logger.logStartAction('translate')
        tokenizer = M2M100Tokenizer.from_pretrained(self.model_name)
        model = M2M100ForConditionalGeneration.from_pretrained(self.model_name)
        tokenizer.src_lang = source_language
        # translat_list_size = segments.size

        for index,seg in enumerate(segments):
            origin_text = seg['text']

             # Check if the translation is already in the cache
            if origin_text in self.translation_cache:
                translated_text = self.translation_cache[origin_text]
            else:
                encoded = tokenizer(origin_text, return_tensors="pt")
                generated_tokens = model.generate(**encoded, forced_bos_token_id=tokenizer.get_lang_id(target_language))
                translated_text = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]

                # Store the translation in the cache
                self.translation_cache[origin_text] = translated_text

            seg['text'] = translated_text
            print(f"Index: {index} From: {origin_text} to {translated_text}")
        self.logger.logEndAction('translate')
        

