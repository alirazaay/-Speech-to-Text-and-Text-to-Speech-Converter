from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QStackedWidget, QLabel
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Translator & STT Pro")
        self.setMinimumSize(1000, 650)
        
        self.init_ui()
        
    def init_ui(self):
        # Main Layout
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setCentralWidget(main_widget)
        
        # Sidebar
        self.sidebar = QWidget()
        self.sidebar.setFixedWidth(220)
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setStyleSheet("QWidget#Sidebar { background-color: #1a1a2e; border-right: 1px solid #2e2e48; }")
        
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        sidebar_layout.setSpacing(10)
        
        # App Title in Sidebar
        title_label = QLabel("AI Translator")
        title_label.setStyleSheet("color: white; font-size: 20px; font-weight: bold; margin-bottom: 20px;")
        title_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(title_label)
        
        # Navigation Buttons
        self.btn_audio = self.create_nav_button("🎙️ Audio Translator")
        self.btn_live = self.create_nav_button("🔴 Live Speech")
        self.btn_pdf = self.create_nav_button("📄 PDF Translator")
        self.btn_history = self.create_nav_button("🕒 History")
        
        sidebar_layout.addWidget(self.btn_audio)
        sidebar_layout.addWidget(self.btn_live)
        sidebar_layout.addWidget(self.btn_pdf)
        sidebar_layout.addWidget(self.btn_history)
        sidebar_layout.addStretch()
        
        # Stacked Widget (Main Content Area)
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background-color: #16213e;")
        
        # Placeholders for Panels
        self.panel_audio = self.create_placeholder_panel("Audio Translator Panel\n(Drag & Drop Audio Files Here)")
        self.panel_live = self.create_placeholder_panel("Live Speech Panel\n(Real-time Dictation)")
        self.panel_pdf = self.create_placeholder_panel("PDF Translator Panel\n(Upload PDF to Translate)")
        self.panel_history = self.create_placeholder_panel("History Panel\n(Past Translations)")
        
        self.stacked_widget.addWidget(self.panel_audio)
        self.stacked_widget.addWidget(self.panel_live)
        self.stacked_widget.addWidget(self.panel_pdf)
        self.stacked_widget.addWidget(self.panel_history)
        
        # Connect buttons
        self.btn_audio.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.btn_live.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.btn_pdf.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.btn_history.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        
        # Add to main layout
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stacked_widget)
        
    def create_nav_button(self, text):
        btn = QPushButton(text)
        btn.setFixedHeight(45)
        btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #e0e0e0;
                border: none;
                text-align: left;
                padding-left: 20px;
                font-size: 14px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2e2e48;
                color: white;
            }
            QPushButton:checked {
                background-color: #8a2be2;
                color: white;
                font-weight: bold;
            }
        """)
        btn.setCheckable(True)
        btn.setAutoExclusive(True)
        return btn

    def create_placeholder_panel(self, text):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        label = QLabel(text)
        label.setStyleSheet("color: #8e8e93; font-size: 24px;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        return widget
