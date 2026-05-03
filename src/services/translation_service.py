from deep_translator import GoogleTranslator
import time

class TranslationService:
    def __init__(self):
        pass

    def translate(self, text, dest_lang="en", src_lang="auto", retries=3):
        """Translates text with basic retry logic."""
        if not text.strip():
            return ""
            
        for attempt in range(retries):
            try:
                # Using deep-translator to bypass Python 3.13 cgi removal issues
                translator = GoogleTranslator(source=src_lang, target=dest_lang)
                return translator.translate(text)
            except Exception as e:
                if attempt == retries - 1:
                    raise Exception(f"Translation failed after {retries} attempts: {e}")
                time.sleep(1) # wait before retry
