import pytest
import json
import os
from playwright.sync_api import Page
from utils.helpers import capture_screenshot

@pytest.fixture(scope="session")
def test_data():
    """Load test data from JSON file"""
    data_file = os.path.join(os.path.dirname(__file__), 'data', 'test_data.json')
    with open(data_file, 'r') as f:
        return json.load(f)

@pytest.fixture
def login_page_setup(page: Page):
    """Navigate to login page before each test"""
    page.goto("https://qa.eyther.ai/login")
    page.wait_for_load_state("networkidle")
    return page

@pytest.fixture(autouse=True)
def screenshot_on_failure(request, page: Page):
    """Take screenshot on test failure"""
    yield
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        screenshot_name = f"{request.node.name}_failure.png"
        capture_screenshot(page, screenshot_name)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results for screenshot fixture"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)