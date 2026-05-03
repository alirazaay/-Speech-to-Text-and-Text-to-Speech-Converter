from googletrans import Translator
import time

class TranslationService:
    def __init__(self):
        self.translator = Translator()

    def translate(self, text, dest_lang="en", src_lang="auto", retries=3):
        """Translates text with basic retry logic."""
        if not text.strip():
            return ""
            
        for attempt in range(retries):
            try:
                # Using googletrans
                result = self.translator.translate(text, dest=dest_lang, src=src_lang)
                return result.text
            except Exception as e:
                if attempt == retries - 1:
                    raise Exception(f"Translation failed after {retries} attempts: {e}")
                time.sleep(1) # wait before retry
