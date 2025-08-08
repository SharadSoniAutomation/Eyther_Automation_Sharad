import os
import base64
from datetime import datetime
from playwright.sync_api import Page

def capture_screenshot(page: Page, filename: str = None):
    """Capture screenshot and return path"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"

    screenshot_dir = "screenshots"
    os.makedirs(screenshot_dir, exist_ok=True)
    screenshot_path = os.path.join(screenshot_dir, filename)
    
    try:
        page.screenshot(path=screenshot_path, timeout=5000)
        return screenshot_path
    except Exception as e:
        print(f"Screenshot capture failed: {e}")
        return None

def screenshot_to_base64(screenshot_path):
    """Convert screenshot to base64 for embedding in HTML"""
    if not screenshot_path or not os.path.exists(screenshot_path):
        return None
    
    try:
        with open(screenshot_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            return f"data:image/png;base64,{encoded_string}"
    except Exception as e:
        print(f"Failed to encode screenshot: {e}")
        return None

def wait_for_element(page: Page, selector: str, timeout: int = 5000):
    """Wait for element to be visible"""
    return page.wait_for_selector(selector, timeout=timeout)

def get_page_title(page: Page):
    """Get current page title"""
    return page.title()

def get_current_url(page: Page):
    """Get current page URL"""
    return page.url