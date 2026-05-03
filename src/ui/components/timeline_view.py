from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QFrame
from PySide6.QtCore import Qt, Signal

class InteractiveBlock(QFrame):
    clicked = Signal(int, int) # start_ms, end_ms

    def __init__(self, transcribed_text, translated_text, start_ms, end_ms):
        super().__init__()
        self.start_ms = start_ms
        self.end_ms = end_ms
        
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            InteractiveBlock {
                background-color: #2e2e48;
                border-radius: 8px;
                margin: 5px;
            }
            InteractiveBlock:hover {
                background-color: #3e3e58;
                border: 1px solid #8a2be2;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        
        lbl_source = QLabel(transcribed_text)
        lbl_source.setWordWrap(True)
        lbl_source.setStyleSheet("color: #aaaaaa; font-size: 12px; font-style: italic;")
        
        lbl_target = QLabel(translated_text)
        lbl_target.setWordWrap(True)
        lbl_target.setStyleSheet("color: white; font-size: 15px; font-weight: bold;")
        
        time_lbl = QLabel(f"{(start_ms/1000):.1f}s - {(end_ms/1000):.1f}s")
        time_lbl.setStyleSheet("color: #8a2be2; font-size: 10px; font-weight: bold;")
        
        layout.addWidget(time_lbl)
        layout.addWidget(lbl_source)
        layout.addWidget(lbl_target)
        
    def mousePressEvent(self, event):
        self.clicked.emit(self.start_ms, self.end_ms)

class TimelineView(QScrollArea):
    play_requested = Signal(int, int)

    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)
        self.setStyleSheet("background-color: transparent; border: none;")
        
        self.container = QWidget()
        self.container.setStyleSheet("background-color: transparent;")
        self.layout = QVBoxLayout(self.container)
        self.layout.setAlignment(Qt.AlignTop)
        
        self.setWidget(self.container)

    def add_block(self, transcribed, translated, start_ms, end_ms):
        block = InteractiveBlock(transcribed, translated, start_ms, end_ms)
        block.clicked.connect(self.play_requested.emit)
        self.layout.addWidget(block)

    def clear(self):
        for i in reversed(range(self.layout.count())): 
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
