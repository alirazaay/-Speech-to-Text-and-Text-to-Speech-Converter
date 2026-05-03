from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QPainter, QColor, QPen, QBrush
from PySide6.QtCore import Qt, QRectF, QThread, Signal
from pydub import AudioSegment

class WaveformLoaderThread(QThread):
    finished = Signal(list)
    
    def __init__(self, file_path, num_bars=200):
        super().__init__()
        self.file_path = file_path
        self.num_bars = num_bars
        
    def run(self):
        try:
            audio = AudioSegment.from_file(self.file_path)
            audio = audio.set_channels(1)
            raw_data = audio.get_array_of_samples()
            
            chunk_size = max(1, len(raw_data) // self.num_bars)
            samples = []
            
            for i in range(0, len(raw_data), chunk_size):
                chunk = raw_data[i:i+chunk_size]
                if len(chunk) > 0:
                    val = max(abs(min(chunk)), abs(max(chunk)))
                    samples.append(val)
                    
            if samples:
                max_val = max(samples)
                if max_val > 0:
                    samples = [s / max_val for s in samples]
                    
            self.finished.emit(samples)
        except Exception as e:
            print(f"Waveform load error: {e}")
            self.finished.emit([])

class WaveformWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.samples = []
        self.loader = None
        self.setMinimumHeight(80)
        self.setStyleSheet("background-color: transparent;")

    def load_audio(self, file_path):
        self.samples = []
        self.update()
        
        self.loader = WaveformLoaderThread(file_path, num_bars=150)
        self.loader.finished.connect(self.on_loaded)
        self.loader.start()

    def on_loaded(self, samples):
        self.samples = samples
        self.update()

    def paintEvent(self, event):
        if not self.samples:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        width = self.width()
        height = self.height()
        
        num_bars = len(self.samples)
        bar_width = max(1, width / num_bars)
        
        painter.setPen(QPen(Qt.NoPen))
        
        for i, val in enumerate(self.samples):
            bar_height = max(4, val * height * 0.9)
            x = i * bar_width
            y = (height - bar_height) / 2
            
            rect = QRectF(x, y, bar_width * 0.7, bar_height)
            
            # Soundcloud-style purple bar
            painter.setBrush(QBrush(QColor("#8a2be2")))
            painter.drawRoundedRect(rect, 2, 2)
