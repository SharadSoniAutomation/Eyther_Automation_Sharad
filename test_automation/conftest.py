
'''import pytest
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

import pytest
import json
import os
from playwright.sync_api import Page
from utils.helpers import capture_screenshot
from pages.login_page import LoginPage

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

@pytest.fixture
def authenticated_session(page: Page, test_data):
    """Fixture that provides an authenticated session"""
    login_page = LoginPage(page)
    
    # Navigate to login page
    login_page.navigate_to_login()
    login_page.wait_for_page_load()
    
    # Perform login
    credentials = test_data["positive_credentials"]
    login_page.login(credentials["email"], credentials["password"])
    
    # Wait for dashboard to load
    page.wait_for_url("**/hospital-owner-dashboard", timeout=10000)
    page.wait_for_load_state("networkidle")
    
    return page

@pytest.fixture(autouse=True)
def screenshot_on_failure(request, page: Page):
    """Take screenshot on test failure with timeout handling"""
    yield
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        try:
            screenshot_name = f"{request.node.name}_failure.png"
            # Use shorter timeout for screenshots
            page.screenshot(path=f"screenshots/{screenshot_name}", timeout=5000)
        except Exception as e:
            print(f"Failed to capture screenshot: {e}")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results for screenshot fixture"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)'''

import pytest
import json
import os
import base64
from datetime import datetime
from playwright.sync_api import Page
from utils.helpers import capture_screenshot
from pages.login_page import LoginPage

# Global test results storage
test_results = []

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

@pytest.fixture
def authenticated_session(page: Page, test_data):
    """Fixture that provides an authenticated session"""
    login_page = LoginPage(page)
    
    # Navigate to login page
    login_page.navigate_to_login()
    login_page.wait_for_page_load()
    
    # Perform login
    credentials = test_data["positive_credentials"]
    login_page.login(credentials["email"], credentials["password"])
    
    # Wait for dashboard to load
    page.wait_for_url("**/hospital-owner-dashboard", timeout=10000)
    page.wait_for_load_state("networkidle")
    
    return page

@pytest.fixture(autouse=True)
def capture_test_results(request, page: Page):
    """Capture comprehensive test results including screenshots and errors"""
    test_start_time = datetime.now()
    screenshot_path = None
    
    yield
    
    test_end_time = datetime.now()
    test_duration = (test_end_time - test_start_time).total_seconds()
    
    # Get test result
    test_passed = True
    error_message = None
    
    if hasattr(request.node, 'rep_call'):
        test_passed = request.node.rep_call.passed
        if not test_passed:
            # Get error details
            if hasattr(request.node.rep_call, 'longrepr') and request.node.rep_call.longrepr:
                error_message = str(request.node.rep_call.longrepr)
            else:
                error_message = "Test failed - no detailed error message available"
            
            # Capture screenshot for failed tests
            try:
                screenshot_filename = f"{request.node.name}_failure_{datetime.now().strftime('%H%M%S')}.png"
                screenshot_path = capture_screenshot(page, screenshot_filename)
                print(f"Screenshot captured: {screenshot_path}")
            except Exception as e:
                print(f"Failed to capture screenshot: {e}")
    
    # Store test result
    test_result = {
        "test_name": request.node.name,
        "test_file": str(request.node.parent).split("::")[-1] if hasattr(request.node, 'parent') else "unknown",
        "status": "PASSED" if test_passed else "FAILED",
        "duration": f"{test_duration:.2f}s",
        "start_time": test_start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": test_end_time.strftime("%Y-%m-%d %H:%M:%S"),
        "error_message": error_message,
        "screenshot_path": screenshot_path,
        "markers": [mark.name for mark in request.node.iter_markers()],
        "module": get_test_module(request.node.name),
        "test_id": request.node.nodeid
    }
    
    test_results.append(test_result)

def get_test_module(test_name):
    """Determine test module based on test name"""
    if 'login' in test_name.lower():
        return 'Login'
    elif 'dashboard' in test_name.lower():
        return 'Dashboard'
    elif 'claim' in test_name.lower():
        return 'Claims'
    else:
        return 'Other'

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

def pytest_sessionfinish(session, exitstatus):
    """Generate comprehensive report at the end of test session"""
    # FIXED: Removed emoji that caused Unicode error
    print("\nGenerating comprehensive test report...")
    
    # Generate the comprehensive report
    try:
        # Import here to avoid import issues
        import sys
        import os
        sys.path.append(os.path.dirname(__file__))
        
        from utils.comprehensive_report_generator import generate_comprehensive_report
        
        report_path = generate_comprehensive_report(test_results)
        print(f"Report generated successfully: {report_path}")
    except Exception as e:
        print(f"Error generating report: {e}")
        # Generate a simple fallback report
        generate_simple_fallback_report(test_results)

def generate_simple_fallback_report(test_results):
    """Generate a simple fallback report if main report fails"""
    print("Generating fallback report...")
    
    total_tests = len(test_results)
    passed_tests = len([t for t in test_results if t['status'] == 'PASSED'])
    failed_tests = len([t for t in test_results if t['status'] == 'FAILED'])
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Test Results - Fallback Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .summary {{ background: #f8f9fa; padding: 20px; margin-bottom: 20px; border-radius: 8px; }}
            .passed {{ color: #28a745; font-weight: bold; }}
            .failed {{ color: #dc3545; font-weight: bold; }}
            .test-item {{ margin: 10px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
            .test-item.failed {{ border-left: 4px solid #dc3545; }}
            .test-item.passed {{ border-left: 4px solid #28a745; }}
        </style>
    </head>
    <body>
        <h1>Test Execution Report - Fallback</h1>
        <div class="summary">
            <h3>Summary</h3>
            <p><strong>Total Tests:</strong> {total_tests}</p>
            <p class="passed">Passed: {passed_tests}</p>
            <p class="failed">Failed: {failed_tests}</p>
            <p><strong>Success Rate:</strong> {(passed_tests/total_tests*100):.1f}%</p>
        </div>
        
        <h3>Test Details</h3>
        {''.join([f'<div class="test-item {t["status"].lower()}"><strong>{t["test_name"]}</strong><br><span class="{t["status"].lower()}">{t["status"]}</span> - Duration: {t["duration"]}<br>Module: {t["module"]}</div>' for t in test_results])}
    </body>
    </html>
    """
    
    os.makedirs("reports", exist_ok=True)
    with open("reports/fallback_report.html", 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("Fallback report generated: reports/fallback_report.html")