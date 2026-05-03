from gtts import gTTS
import os

class TTSService:
    def generate_audio(self, text, dest_lang="en", output_path="output.mp3"):
        """Generates an mp3 file from text using gTTS."""
        if not text.strip():
            raise ValueError("Text is empty.")
            
        try:
            tts = gTTS(text=text, lang=dest_lang, slow=False)
            tts.save(output_path)
            return output_path
        except Exception as e:
            raise Exception(f"TTS generation failed: {e}")
