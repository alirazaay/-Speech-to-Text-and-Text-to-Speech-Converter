from PySide6.QtCore import QThread, Signal
from services.stt_service import STTService
from services.translation_service import TranslationService
from services.tts_service import TTSService
from processing.audio_processor import AudioProcessor
from processing.pdf_processor import PDFProcessor
import os

class AudioTranslationWorker(QThread):
    progress = Signal(int, str) 
    finished = Signal(str, str, str) 
    error = Signal(str)

    def __init__(self, file_path, source_lang, target_lang):
        super().__init__()
        self.file_path = file_path
        self.source_lang = source_lang
        self.target_lang = target_lang

        self.audio_processor = AudioProcessor()
        self.stt_service = STTService()
        self.translation_service = TranslationService()
        self.tts_service = TTSService()

    def run(self):
        try:
            self.progress.emit(10, "Converting audio format...")
            wav_path = self.audio_processor.convert_to_wav(self.file_path)
            
            self.progress.emit(30, "Transcribing audio (This may take a while)...")
            # Google STT language codes: en-US, es-ES, etc.
            stt_lang = "en-US" if self.source_lang == "en" else self.source_lang
            transcribed = self.stt_service.transcribe_audio_file(wav_path, language=stt_lang)
            
            self.progress.emit(60, "Translating text...")
            translated = self.translation_service.translate(transcribed, dest_lang=self.target_lang, src_lang=self.source_lang)
            
            self.progress.emit(85, "Generating TTS...")
            output_dir = os.path.dirname(self.file_path)
            out_audio = os.path.join(output_dir, "translated_audio_out.mp3")
            self.tts_service.generate_audio(translated, dest_lang=self.target_lang, output_path=out_audio)
            
            self.progress.emit(100, "Done!")
            self.finished.emit(transcribed, translated, out_audio)
        except Exception as e:
            self.error.emit(str(e))


class LiveSpeechWorker(QThread):
    progress = Signal(str)
    finished = Signal(str, str, str)
    error = Signal(str)

    def __init__(self, source_lang, target_lang):
        super().__init__()
        self.source_lang = source_lang
        self.target_lang = target_lang
        
        self.stt_service = STTService()
        self.translation_service = TranslationService()
        self.tts_service = TTSService()

    def run(self):
        try:
            self.progress.emit("Listening... Please speak now.")
            stt_lang = "en-US" if self.source_lang == "en" else self.source_lang
            transcribed = self.stt_service.listen_and_transcribe(language=stt_lang)
            
            if transcribed in ["No speech detected", "Could not understand audio"]:
                self.error.emit(transcribed)
                return
                
            self.progress.emit("Translating...")
            translated = self.translation_service.translate(transcribed, dest_lang=self.target_lang, src_lang=self.source_lang)
            
            self.progress.emit("Generating Audio...")
            out_audio = "live_translated.mp3"
            self.tts_service.generate_audio(translated, dest_lang=self.target_lang, output_path=out_audio)
            
            self.progress.emit("Done!")
            self.finished.emit(transcribed, translated, out_audio)
        except Exception as e:
            self.error.emit(str(e))


class PDFTranslationWorker(QThread):
    progress = Signal(int, str)
    finished = Signal(str, str)
    error = Signal(str)

    def __init__(self, file_path, source_lang, target_lang):
        super().__init__()
        self.file_path = file_path
        self.source_lang = source_lang
        self.target_lang = target_lang
        
        self.pdf_processor = PDFProcessor()
        self.translation_service = TranslationService()

    def run(self):
        try:
            self.progress.emit(20, "Extracting text from PDF...")
            extracted_text = self.pdf_processor.extract_text(self.file_path)
            
            if not extracted_text:
                raise Exception("No text found in PDF.")
                
            self.progress.emit(60, "Translating text...")
            # For large PDFs, we should chunk the text. For now, basic translation.
            translated = self.translation_service.translate(extracted_text, dest_lang=self.target_lang, src_lang=self.source_lang)
            
            self.progress.emit(100, "Done!")
            self.finished.emit(extracted_text, translated)
        except Exception as e:
            self.error.emit(str(e))
