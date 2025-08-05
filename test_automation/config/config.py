import os

class Config:
    BASE_URL = "https://qa.eyther.ai"
    LOGIN_URL = f"{BASE_URL}/login"
    BROWSER = "chromium"
    HEADLESS = False
    TIMEOUT = 30000
    SCREENSHOT_DIR = "screenshots"
    
    # Create screenshot directory if it doesn't exist
    @classmethod
    def setup_directories(cls):
        os.makedirs(cls.SCREENSHOT_DIR, exist_ok=True)