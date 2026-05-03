import sys
import os
from PySide6.QtWidgets import QApplication
import qdarktheme

from core.config import Config
from ui.main_window import MainWindow

def main():
    # Ensure the database directory exists
    os.makedirs(os.path.dirname(Config.DB_PATH), exist_ok=True)
    
    app = QApplication(sys.argv)
    
    # Apply modern dark theme
    qdarktheme.setup_theme("dark", custom_colors={"primary": "#8a2be2"}) # Deep purple accent
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
