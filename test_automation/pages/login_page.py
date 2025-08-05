from playwright.sync_api import Page, expect

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.email_input = page.locator("//input[@id='email']")
        self.password_input = page.locator("//input[@id='password']")
        self.login_button = page.locator("//button[normalize-space()='Log in']")
        self.forgot_password_link = page.locator("//a[normalize-space()='Forgot Password?']")
        self.error_message = page.locator("//div[@id='5']")
        
    def navigate_to_login(self):
        """Navigate to login page"""
        self.page.goto("https://qa.eyther.ai/login")
        
    def enter_email(self, email: str):
        """Enter email in email field"""
        self.email_input.fill(email)
        
    def enter_password(self, password: str):
        """Enter password in password field"""
        self.password_input.fill(password)
        
    def click_login(self):
        """Click login button"""
        self.login_button.click()
        
    def click_forgot_password(self):
        """Click forgot password link"""
        self.forgot_password_link.click()
        
    def login(self, email: str, password: str):
        """Perform complete login action"""
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()
        
    def get_error_message(self):
        """Get error message text"""
        return self.error_message.inner_text()
        
    def is_login_successful(self):
        """Check if login was successful by URL change or dashboard elements"""
        return self.page.url != "https://qa.eyther.ai/login"
        
    def wait_for_page_load(self):
        """Wait for page to load completely"""
        self.page.wait_for_load_state("networkidle")