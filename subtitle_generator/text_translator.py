from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

class TextTranslator:
    def __init__(self, model_name="facebook/m2m100_418M"):
        self.model_name = model_name

    def translate(self, text, source_language, target_language):
        with M2M100Tokenizer.from_pretrained(self.model_name) as tokenizer, \
             M2M100ForConditionalGeneration.from_pretrained(self.model_name) as model:
            tokenizer.src_lang = source_language
            encoded = tokenizer(text, return_tensors="pt")
            generated_tokens = model.generate(**encoded, forced_bos_token_id=tokenizer.get_lang_id(target_language))
            return tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]

