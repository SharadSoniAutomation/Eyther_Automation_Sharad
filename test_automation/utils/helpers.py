import os
from datetime import datetime
from playwright.sync_api import Page

def capture_screenshot(page: Page, filename: str = None):
    """Capture screenshot and save to screenshots directory"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
    
    screenshot_path = os.path.join("screenshots", filename)
    os.makedirs("screenshots", exist_ok=True)
    page.screenshot(path=screenshot_path)
    return screenshot_path

def wait_for_element(page: Page, selector: str, timeout: int = 5000):
    """Wait for element to be visible"""
    return page.wait_for_selector(selector, timeout=timeout)

def get_page_title(page: Page):
    """Get current page title"""
    return page.title()

def get_current_url(page: Page):
    """Get current page URL"""
    return page.url