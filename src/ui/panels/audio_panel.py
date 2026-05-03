from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QComboBox, QTextEdit, QFileDialog, QProgressBar
)
from PySide6.QtCore import Qt
from core.workers import AudioTranslationWorker
from core.config import Config

class AudioPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.file_path = None
        self.worker = None
        self.setAcceptDrops(True)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        title = QLabel("🎙️ Audio File Translator")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        layout.addWidget(title)

        # File Selection
        file_layout = QHBoxLayout()
        self.lbl_file = QLabel("No file selected")
        self.lbl_file.setStyleSheet("color: #aaaaaa; border: 1px dashed #555; padding: 10px; border-radius: 5px;")
        btn_select = QPushButton("Select Audio File")
        btn_select.setStyleSheet("padding: 10px; background-color: #2e2e48; color: white; border-radius: 5px;")
        btn_select.clicked.connect(self.select_file)
        file_layout.addWidget(self.lbl_file, stretch=1)
        file_layout.addWidget(btn_select)
        layout.addLayout(file_layout)

        # Languages
        lang_layout = QHBoxLayout()
        self.cmb_source = QComboBox()
        self.cmb_source.addItems(["en", "es", "zh-CN", "ja", "fr", "de"])
        self.cmb_target = QComboBox()
        self.cmb_target.addItems(["es", "en", "zh-CN", "ja", "fr", "de"])
        
        lang_layout.addWidget(QLabel("Source:"))
        lang_layout.addWidget(self.cmb_source)
        lang_layout.addWidget(QLabel("Target:"))
        lang_layout.addWidget(self.cmb_target)
        lang_layout.addStretch()
        layout.addLayout(lang_layout)

        # Waveform Visualizer
        from ui.components.waveform import WaveformWidget
        self.waveform = WaveformWidget()
        layout.addWidget(self.waveform)

        # Progress
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.hide()
        self.lbl_status = QLabel("")
        self.lbl_status.setStyleSheet("color: #8a2be2;")
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.lbl_status)

        # Output (Timeline View)
        from ui.components.timeline_view import TimelineView
        self.timeline_view = TimelineView()
        self.timeline_view.play_requested.connect(self.play_audio_segment)
        layout.addWidget(self.timeline_view)

        # Action Buttons
        self.btn_translate = QPushButton("Translate")
        self.btn_translate.setStyleSheet("padding: 12px; background-color: #8a2be2; color: white; border-radius: 5px; font-weight: bold;")
        self.btn_translate.clicked.connect(self.start_translation)
        layout.addWidget(self.btn_translate)

    def play_audio_segment(self, start_ms, end_ms):
        # We will implement QMediaPlayer or simple audio playback here later
        print(f"Playing segment: {start_ms}ms to {end_ms}ms")

    def select_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Audio", Config.DATA_DIR, "Audio Files (*.mp3 *.wav *.ogg *.m4a *.flac)")
        if path:
            self.file_path = path
            self.lbl_file.setText(path.split("/")[-1])
            self.waveform.load_audio(path)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
            self.lbl_file.setStyleSheet("color: white; border: 2px dashed #8a2be2; background-color: #2a2a4a; padding: 10px; border-radius: 5px;")
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.lbl_file.setStyleSheet("color: #aaaaaa; border: 1px dashed #555; padding: 10px; border-radius: 5px;")

    def dropEvent(self, event):
        self.dragLeaveEvent(event)
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if files:
            path = files[0]
            if path.lower().endswith(('.mp3', '.wav', '.ogg', '.m4a', '.flac')):
                self.file_path = path
                self.lbl_file.setText(path.split("/")[-1] if "/" in path else path.split("\\")[-1])
                self.waveform.load_audio(path)
            else:
                self.lbl_status.setText("Invalid file format. Please drop an audio file.")

    def start_translation(self):
        if not self.file_path:
            self.lbl_status.setText("Please select a file first.")
            return

        self.btn_translate.setEnabled(False)
        self.progress_bar.setValue(0)
        self.progress_bar.show()
        self.timeline_view.clear()

        source = self.cmb_source.currentText()
        target = self.cmb_target.currentText()

        self.worker = AudioTranslationWorker(self.file_path, source, target)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def update_progress(self, val, msg):
        self.progress_bar.setValue(val)
        self.lbl_status.setText(msg)

    def on_finished(self, transcribed, translated, audio_out):
        self.progress_bar.hide()
        self.lbl_status.setText(f"Success! Audio saved to: {audio_out}")
        
        # In a fully chunked system, the worker would emit chunks. 
        # Since we're bridging the old monolithic API, we add the whole block as one chunk.
        self.timeline_view.add_block(transcribed, translated, 0, 5000)
        
        self.btn_translate.setEnabled(True)

    def on_error(self, err):
        self.progress_bar.hide()
        self.lbl_status.setText(f"Error: {err}")
        self.btn_translate.setEnabled(True)
