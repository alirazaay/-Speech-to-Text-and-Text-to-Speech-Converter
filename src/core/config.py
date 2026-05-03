import os

class Config:
    APP_NAME = "AI Translator & STT"
    APP_VERSION = "2.0.0"
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    DB_PATH = os.path.join(DATA_DIR, "history.db")
    
    # Default settings
    DEFAULT_SOURCE_LANG = "en"
    DEFAULT_TARGET_LANG = "es"
