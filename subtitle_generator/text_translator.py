from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

class TextTranslator:
    def __init__(self, model_name="facebook/m2m100_418M"):
        self.model_name = model_name

    # Translate multiple text lines
    def translate(self, segments, source_language, target_language):
        tokenizer = M2M100Tokenizer.from_pretrained(self.model_name)
        model = M2M100ForConditionalGeneration.from_pretrained(self.model_name)
        tokenizer.src_lang = source_language

        for seg in segments:
            origin_text = seg['text']
            encoded = tokenizer(origin_text, return_tensors="pt")
            generated_tokens = model.generate(**encoded, forced_bos_token_id=tokenizer.get_lang_id(target_language))
            translated_text = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]

            seg['text'] = translated_text
            print(f"From: {origin_text} to {translated_text}")
        

