from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QComboBox, QTextEdit, QFileDialog, QProgressBar
)
from core.workers import PDFTranslationWorker
from core.config import Config

class PDFPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.file_path = None
        self.worker = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        title = QLabel("📄 PDF Translator")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        layout.addWidget(title)

        # File Selection
        file_layout = QHBoxLayout()
        self.lbl_file = QLabel("No PDF selected")
        self.lbl_file.setStyleSheet("color: #aaaaaa; border: 1px dashed #555; padding: 10px; border-radius: 5px;")
        btn_select = QPushButton("Select PDF")
        btn_select.setStyleSheet("padding: 10px; background-color: #2e2e48; color: white; border-radius: 5px;")
        btn_select.clicked.connect(self.select_file)
        file_layout.addWidget(self.lbl_file, stretch=1)
        file_layout.addWidget(btn_select)
        layout.addLayout(file_layout)

        # Languages
        lang_layout = QHBoxLayout()
        self.cmb_source = QComboBox()
        self.cmb_source.addItems(["es", "en", "zh-CN", "ja"])
        self.cmb_target = QComboBox()
        self.cmb_target.addItems(["en", "es", "zh-CN", "ja"])
        
        lang_layout.addWidget(QLabel("Source:"))
        lang_layout.addWidget(self.cmb_source)
        lang_layout.addWidget(QLabel("Target:"))
        lang_layout.addWidget(self.cmb_target)
        lang_layout.addStretch()
        layout.addLayout(lang_layout)

        # Progress
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.hide()
        self.lbl_status = QLabel("")
        self.lbl_status.setStyleSheet("color: #8a2be2;")
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.lbl_status)

        # Output
        self.txt_output = QTextEdit()
        self.txt_output.setReadOnly(True)
        self.txt_output.setPlaceholderText("Translation output will appear here...")
        self.txt_output.setStyleSheet("background-color: #1a1a2e; border: 1px solid #333; border-radius: 8px; padding: 10px;")
        layout.addWidget(self.txt_output)

        # Action Buttons
        self.btn_translate = QPushButton("Translate PDF")
        self.btn_translate.setStyleSheet("padding: 12px; background-color: #8a2be2; color: white; border-radius: 5px; font-weight: bold;")
        self.btn_translate.clicked.connect(self.start_translation)
        layout.addWidget(self.btn_translate)

    def select_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select PDF", Config.DATA_DIR, "PDF Files (*.pdf)")
        if path:
            self.file_path = path
            self.lbl_file.setText(path.split("/")[-1])

    def start_translation(self):
        if not self.file_path:
            self.lbl_status.setText("Please select a PDF first.")
            return

        self.btn_translate.setEnabled(False)
        self.progress_bar.setValue(0)
        self.progress_bar.show()
        self.txt_output.clear()

        source = self.cmb_source.currentText()
        target = self.cmb_target.currentText()

        self.worker = PDFTranslationWorker(self.file_path, source, target)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def update_progress(self, val, msg):
        self.progress_bar.setValue(val)
        self.lbl_status.setText(msg)

    def on_finished(self, extracted, translated):
        self.progress_bar.hide()
        self.lbl_status.setText("Success!")
        self.txt_output.setText(f"--- EXTRACTED ---\n{extracted}\n\n--- TRANSLATED ---\n{translated}")
        self.btn_translate.setEnabled(True)

    def on_error(self, err):
        self.progress_bar.hide()
        self.lbl_status.setText(f"Error: {err}")
        self.btn_translate.setEnabled(True)
