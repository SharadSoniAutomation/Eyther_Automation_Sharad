

from playwright.sync_api import Page, expect, TimeoutError

class DashboardPage:
    def __init__(self, page: Page):
        self.page = page
        
        # Navigation elements with multiple selector options
        self.dashboard_link = page.locator("//a[@href='/hospital-owner-dashboard']")
        self.claim_management_link = page.locator("//a[@href='/claims/hospital']")
        
        # Multiple logout button selectors for better reliability
        self.logout_button = page.locator("//button[normalize-space()='Logout']")
        self.logout_button_alt = page.locator("button:has-text('Logout')")
        
        # Dashboard elements
        self.dashboard_heading = page.locator("//h1[normalize-space()='Hospital Owner Dashboard']")
        self.welcome_message = page.locator("(//div[@class='text-[16px] font-roboto font-medium'])[1]")
        self.user_email = page.locator("//div[contains(text(), 'SS_Hos@gmail.com')]")
        self.profile_button = page.locator("//button[@class='px-4 py-1 hover:cursor-pointer']//*[name()='svg']")
        
        # Content elements
        self.loading_message = page.locator("//div[contains(text(), 'Thanks for waiting — we're getting things ready')]")
        self.eyther_logo = page.locator("//h3[normalize-space()='Eyther.']")

    def navigate_to_dashboard(self):
        """Navigate to dashboard page"""
        self.page.goto("https://qa.eyther.ai/hospital-owner-dashboard")
        self.page.wait_for_load_state("networkidle")

    def navigate_to_claim_management(self):
        """Navigate to claim management page"""
        self.claim_management_link.click()
        self.page.wait_for_url("**/claims/hospital")

    def logout(self):
        """Perform logout with improved error handling"""
        try:
            # Try primary logout button
            if self.logout_button.is_visible(timeout=5000):
                self.logout_button.click()
            else:
                # Try alternative logout button
                self.logout_button_alt.click()
            
            # Wait for navigation
            self.page.wait_for_url("**/login", timeout=10000)
            
        except TimeoutError:
            # If standard selectors fail, try JavaScript
            self.page.evaluate("""
                const logoutButtons = Array.from(document.querySelectorAll('button'))
                    .filter(btn => btn.textContent.toLowerCase().includes('logout'));
                if (logoutButtons.length > 0) {
                    logoutButtons[0].click();
                }
            """)
            # Wait for navigation after JS click
            try:
                self.page.wait_for_url("**/login", timeout=10000)
            except TimeoutError:
                raise Exception("Logout failed - could not navigate to login page")

    def is_dashboard_loaded(self):
        """Check if dashboard is fully loaded"""
        try:
            return (self.dashboard_heading.is_visible(timeout=5000) and 
                   "/hospital-owner-dashboard" in self.page.url)
        except TimeoutError:
            return False

    def get_welcome_message_text(self):
        """Get welcome message text with error handling"""
        try:
            return self.welcome_message.inner_text(timeout=5000)
        except TimeoutError:
            return ""

    def get_user_email_text(self):
        """Get user email text with error handling"""
        try:
            return self.user_email.inner_text(timeout=5000)
        except TimeoutError:
            return ""

    def wait_for_dashboard_load(self):
        """Wait for dashboard to load completely with improved error handling"""
        # Wait for network to be idle
        self.page.wait_for_load_state("networkidle")
        
        # Wait for dashboard heading with timeout
        try:
            self.dashboard_heading.wait_for(state="visible", timeout=10000)
        except TimeoutError:
            # If heading not found, check if we're on the right page
            if "/hospital-owner-dashboard" not in self.page.url:
                raise Exception(f"Not on dashboard page. Current URL: {self.page.url}")
            else:
                # Page is correct but heading might have different text/selector
                print("Warning: Dashboard heading not found, but URL indicates dashboard page")

    def is_loading_message_visible(self):
        """Check if loading message is visible with timeout handling"""
        try:
            return self.loading_message.is_visible(timeout=3000)
        except TimeoutError:
            return False

    def wait_for_loading_to_complete(self):
        """Wait for loading message to disappear"""
        try:
            # Wait for loading message to appear (if it does)
            if self.loading_message.is_visible(timeout=2000):
                # Then wait for it to disappear
                self.loading_message.wait_for(state="hidden", timeout=15000)
        except TimeoutError:
            # Loading message might not appear or might already be gone
            pass

    def get_logout_button(self):
        """Get logout button with fallback options"""
        logout_selectors = [
            "//button[normalize-space()='Logout']",
            "button:has-text('Logout')",
            "[data-testid='logout-button']",
            "button[type='button']:has-text('Logout')",
            ".logout-btn"
        ]
        
        for selector in logout_selectors:
            try:
                element = self.page.locator(selector)
                if element.is_visible(timeout=2000):
                    return element
            except TimeoutError:
                continue
        
        raise Exception("Logout button not found with any selector")

    def verify_dashboard_elements(self):
        """Verify all essential dashboard elements are present"""
        elements_status = {
            'dashboard_heading': False,
            'welcome_message': False,
            'user_email': False,
            'logout_button': False
        }
        
        try:
            elements_status['dashboard_heading'] = self.dashboard_heading.is_visible(timeout=5000)
        except TimeoutError:
            pass
            
        try:
            elements_status['welcome_message'] = self.welcome_message.is_visible(timeout=5000)
        except TimeoutError:
            pass
            
        try:
            elements_status['user_email'] = self.user_email.is_visible(timeout=5000)
        except TimeoutError:
            pass
            
        try:
            logout_btn = self.get_logout_button()
            elements_status['logout_button'] = logout_btn.is_visible()
        except:
            pass
        
        return elements_status