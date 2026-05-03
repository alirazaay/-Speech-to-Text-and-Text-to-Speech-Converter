import os
import ffmpeg
from pydub import AudioSegment

class AudioProcessor:
    def convert_to_wav(self, input_file, output_file=None):
        """Converts an audio file to WAV format for SpeechRecognition compatibility."""
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"File not found: {input_file}")
            
        ext = os.path.splitext(input_file)[-1].lower()
        if not output_file:
            output_file = input_file.replace(ext, ".wav")
            
        if ext == ".wav":
            # Just copy or return the original if it's already a wav
            return input_file

        try:
            # Using ffmpeg-python and pydub
            if ext in [".mp3", ".ogg", ".m4a", ".flac"]:
                # pydub can handle this cleanly if ffmpeg is in PATH
                audio = AudioSegment.from_file(input_file)
                audio.export(output_file, format="wav")
                return output_file
            else:
                raise ValueError(f"Unsupported audio format: {ext}")
        except Exception as e:
            raise Exception(f"Audio conversion failed: {e}")
