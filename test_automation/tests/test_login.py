

import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from utils.helpers import capture_screenshot

class TestLogin:
    
    @pytest.mark.positive
    def test_valid_login_credentials(self, login_page_setup: Page, test_data):
        """Test login with valid credentials"""
        login_page = LoginPage(login_page_setup)
        login_page.wait_for_page_load()
        
        credentials = test_data["positive_credentials"]
        login_page.login(credentials["email"], credentials["password"])
        
        # Wait for navigation and verify login success
        login_page_setup.wait_for_timeout(3000)
        assert login_page.is_login_successful(), "Login should be successful"
        capture_screenshot(login_page_setup, "valid_login_success.png")
    
    @pytest.mark.positive
    def test_email_field_accepts_valid_email(self, login_page_setup: Page, test_data):
        """Test email field accepts valid email format"""
        login_page = LoginPage(login_page_setup)
        credentials = test_data["positive_credentials"]
        
        login_page.enter_email(credentials["email"])
        email_value = login_page.email_input.input_value()
        assert email_value == credentials["email"], "Email should be entered correctly"
    
    @pytest.mark.positive
    def test_password_field_accepts_valid_password(self, login_page_setup: Page, test_data):
        """Test password field accepts valid password"""
        login_page = LoginPage(login_page_setup)
        credentials = test_data["positive_credentials"]
        
        login_page.enter_password(credentials["password"])
        password_value = login_page.password_input.input_value()
        assert password_value == credentials["password"], "Password should be entered correctly"
    
    @pytest.mark.positive
    def test_login_button_is_clickable(self, login_page_setup: Page):
        """Test login button is clickable"""
        login_page = LoginPage(login_page_setup)
        
        expect(login_page.login_button).to_be_enabled()
        expect(login_page.login_button).to_be_visible()
    
    @pytest.mark.positive
    def test_forgot_password_link_exists(self, login_page_setup: Page):
        """Test forgot password link is present and clickable"""
        login_page = LoginPage(login_page_setup)
        
        expect(login_page.forgot_password_link).to_be_visible()
        expect(login_page.forgot_password_link).to_be_enabled()
    
    @pytest.mark.positive
    def test_login_form_elements_present(self, login_page_setup: Page):
        """Test all login form elements are present"""
        login_page = LoginPage(login_page_setup)
        
        expect(login_page.email_input).to_be_visible()
        expect(login_page.password_input).to_be_visible()
        expect(login_page.login_button).to_be_visible()
    
    @pytest.mark.positive
    def test_page_title_correct(self, login_page_setup: Page):
        """Test login page has correct title"""
        expected_title = "Eyther - Accelerate Claim Processing with AI"
        actual_title = login_page_setup.title()
        assert expected_title in actual_title, f"Page title should contain '{expected_title}'"
    
    @pytest.mark.positive
    def test_ssl_encryption_message_displayed(self, login_page_setup: Page):
        """Test SSL encryption message is displayed"""
        ssl_message = login_page_setup.locator("text=Protected by SSL encryption")
        expect(ssl_message).to_be_visible()
    
   
    
    
    @pytest.mark.positive
    def test_password_field_type(self, login_page_setup: Page):
        """Test password field has correct type attribute"""
        login_page = LoginPage(login_page_setup)
        field_type = login_page.password_input.get_attribute("type")
        assert field_type == "password", "Password field should have type='password'"
    
    # Negative Test Cases
    
    @pytest.mark.negative
    def test_invalid_email_format(self, login_page_setup: Page, test_data):
        """Test login with invalid email format"""
        login_page = LoginPage(login_page_setup)
        test_case = test_data["negative_test_cases"][0]
        
        login_page.login(test_case["email"], test_case["password"])
        login_page_setup.wait_for_timeout(2000)
        
        # Check if login failed (still on login page)
        assert not login_page.is_login_successful(), "Login should fail with invalid email"
        capture_screenshot(login_page_setup, "invalid_email_format.png")
    
    @pytest.mark.negative
    def test_empty_email_field(self, login_page_setup: Page, test_data):
        """Test login with empty email field"""
        login_page = LoginPage(login_page_setup)
        test_case = test_data["negative_test_cases"][1]
        
        login_page.login(test_case["email"], test_case["password"])
        login_page_setup.wait_for_timeout(2000)
        
        assert not login_page.is_login_successful(), "Login should fail with empty email"
        capture_screenshot(login_page_setup, "empty_email_field.png")
    
    @pytest.mark.negative
    def test_empty_password_field(self, login_page_setup: Page, test_data):
        """Test login with empty password field"""
        login_page = LoginPage(login_page_setup)
        test_case = test_data["negative_test_cases"][2]
        
        login_page.login(test_case["email"], test_case["password"])
        login_page_setup.wait_for_timeout(2000)
        
        assert not login_page.is_login_successful(), "Login should fail with empty password"
        capture_screenshot(login_page_setup, "empty_password_field.png")
    
    @pytest.mark.negative
    def test_both_fields_empty(self, login_page_setup: Page, test_data):
        """Test login with both fields empty"""
        login_page = LoginPage(login_page_setup)
        test_case = test_data["negative_test_cases"][3]
        
        login_page.login(test_case["email"], test_case["password"])
        login_page_setup.wait_for_timeout(2000)
        
        assert not login_page.is_login_successful(), "Login should fail with both fields empty"
        capture_screenshot(login_page_setup, "both_fields_empty.png")
    
    @pytest.mark.negative
    def test_wrong_email_valid_password(self, login_page_setup: Page, test_data):
        """Test login with wrong email but valid password"""
        login_page = LoginPage(login_page_setup)
        test_case = test_data["negative_test_cases"][4]
        
        login_page.login(test_case["email"], test_case["password"])
        login_page_setup.wait_for_timeout(2000)
        
        assert not login_page.is_login_successful(), "Login should fail with wrong email"
        capture_screenshot(login_page_setup, "wrong_email.png")
    
    @pytest.mark.negative
    def test_valid_email_wrong_password(self, login_page_setup: Page, test_data):
        """Test login with valid email but wrong password"""
        login_page = LoginPage(login_page_setup)
        test_case = test_data["negative_test_cases"][5]
        
        login_page.login(test_case["email"], test_case["password"])
        login_page_setup.wait_for_timeout(2000)
        
        assert not login_page.is_login_successful(), "Login should fail with wrong password"
        capture_screenshot(login_page_setup, "wrong_password.png")
    
    @pytest.mark.negative
    def test_sql_injection_attempt(self, login_page_setup: Page, test_data):
        """Test login with SQL injection attempt"""
        login_page = LoginPage(login_page_setup)
        test_case = test_data["negative_test_cases"][6]
        
        login_page.login(test_case["email"], test_case["password"])
        login_page_setup.wait_for_timeout(2000)
        
        assert not login_page.is_login_successful(), "Login should fail with SQL injection attempt"
        capture_screenshot(login_page_setup, "sql_injection_attempt.png")
    
    @pytest.mark.negative
    def test_xss_attempt(self, login_page_setup: Page, test_data):
        """Test login with XSS attempt"""
        login_page = LoginPage(login_page_setup)
        test_case = test_data["negative_test_cases"][7]
        
        login_page.login(test_case["email"], test_case["password"])
        login_page_setup.wait_for_timeout(2000)
        
        assert not login_page.is_login_successful(), "Login should fail with XSS attempt"
        capture_screenshot(login_page_setup, "xss_attempt.png")
    
    @pytest.mark.negative
    def test_very_long_email(self, login_page_setup: Page, test_data):
        """Test login with very long email"""
        login_page = LoginPage(login_page_setup)
        test_case = test_data["negative_test_cases"][8]
        
        login_page.login(test_case["email"], test_case["password"])
        login_page_setup.wait_for_timeout(2000)
        
        assert not login_page.is_login_successful(), "Login should fail with very long email"
        capture_screenshot(login_page_setup, "very_long_email.png")
    
    @pytest.mark.negative
    def test_very_long_password(self, login_page_setup: Page, test_data):
        """Test login with very long password"""
        login_page = LoginPage(login_page_setup)
        test_case = test_data["negative_test_cases"][9]
        
        login_page.login(test_case["email"], test_case["password"])
        login_page_setup.wait_for_timeout(2000)
        
        assert not login_page.is_login_successful(), "Login should fail with very long password"
        capture_screenshot(login_page_setup, "very_long_password.png")


# How to run tests:
# pytest tests/test_login.py -v --headed --browser=chromium
# pytest tests/test_login.py -m positive -v  # Run only positive tests
# pytest tests/test_login.py -m negative -v  # Run only negative tests
# pytest tests/test_login.py --screenshot=on --video=on  # With screenshots and videos