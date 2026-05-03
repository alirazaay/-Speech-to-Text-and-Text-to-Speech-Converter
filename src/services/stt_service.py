import speech_recognition as sr
import os

class STTService:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def transcribe_audio_file(self, file_path, language="en"):
        """Transcribes a wav file using Google Web Speech API."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found: {file_path}")

        try:
            with sr.AudioFile(file_path) as source:
                audio_data = self.recognizer.record(source)
                
            text = self.recognizer.recognize_google(audio_data, language=language)
            return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            raise Exception(f"Could not request results from Google STT service; {e}")

    def listen_and_transcribe(self, language="en", timeout=5):
        """Listens to the microphone and transcribes."""
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio_data = self.recognizer.listen(source, timeout=timeout)
                
            text = self.recognizer.recognize_google(audio_data, language=language)
            return text
        except sr.WaitTimeoutError:
            return "No speech detected"
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            raise Exception(f"Could not request results from Google STT service; {e}")
