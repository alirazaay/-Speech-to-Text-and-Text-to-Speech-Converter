from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QComboBox, QTextEdit
)
from core.workers import LiveSpeechWorker

class LivePanel(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        title = QLabel("🔴 Live Speech Translator")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        layout.addWidget(title)

        # Languages
        lang_layout = QHBoxLayout()
        self.cmb_source = QComboBox()
        self.cmb_source.addItems(["en", "es", "zh-CN", "ja"])
        self.cmb_target = QComboBox()
        self.cmb_target.addItems(["es", "en", "zh-CN", "ja"])
        
        lang_layout.addWidget(QLabel("Source:"))
        lang_layout.addWidget(self.cmb_source)
        lang_layout.addWidget(QLabel("Target:"))
        lang_layout.addWidget(self.cmb_target)
        lang_layout.addStretch()
        layout.addLayout(lang_layout)

        # Status
        self.lbl_status = QLabel("Ready")
        self.lbl_status.setStyleSheet("color: #8a2be2; font-size: 16px;")
        layout.addWidget(self.lbl_status)

        # Output
        self.txt_output = QTextEdit()
        self.txt_output.setReadOnly(True)
        self.txt_output.setPlaceholderText("Live translation output will appear here...")
        self.txt_output.setStyleSheet("background-color: #1a1a2e; border: 1px solid #333; border-radius: 8px; padding: 10px;")
        layout.addWidget(self.txt_output)

        # Action Buttons
        self.btn_record = QPushButton("Start Recording")
        self.btn_record.setStyleSheet("padding: 12px; background-color: #e63946; color: white; border-radius: 5px; font-weight: bold;")
        self.btn_record.clicked.connect(self.start_recording)
        layout.addWidget(self.btn_record)

    def start_recording(self):
        self.btn_record.setEnabled(False)
        self.txt_output.clear()

        source = self.cmb_source.currentText()
        target = self.cmb_target.currentText()

        self.worker = LiveSpeechWorker(source, target)
        self.worker.progress.connect(self.update_status)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def update_status(self, msg):
        self.lbl_status.setText(msg)

    def on_finished(self, transcribed, translated, audio_out):
        self.lbl_status.setText(f"Success! Audio saved to: {audio_out}")
        self.txt_output.setText(f"--- TRANSCRIBED ---\n{transcribed}\n\n--- TRANSLATED ---\n{translated}")
        self.btn_record.setEnabled(True)

    def on_error(self, err):
        self.lbl_status.setText(f"Error: {err}")
        self.btn_record.setEnabled(True)
