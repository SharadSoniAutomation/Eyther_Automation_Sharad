from playwright.sync_api import Page, expect

class DashboardPage:
    def __init__(self, page: Page):
        self.page = page
        
        # Navigation elements
        self.dashboard_link = page.locator("//a[@href='/hospital-owner-dashboard']")
        self.claim_management_link = page.locator("//a[@href='/claims/hospital']")
        self.logout_button = page.locator("//button[normalize-space()='Logout']")
        
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
        """Perform logout"""
        self.logout_button.click()
        self.page.wait_for_url("**/login")

    def is_dashboard_loaded(self):
        """Check if dashboard is fully loaded"""
        return self.dashboard_heading.is_visible() and "/hospital-owner-dashboard" in self.page.url

    def get_welcome_message_text(self):
        """Get welcome message text"""
        return self.welcome_message.inner_text()

    def get_user_email_text(self):
        """Get user email text"""
        return self.user_email.inner_text()

    def wait_for_dashboard_load(self):
        """Wait for dashboard to load completely"""
        self.page.wait_for_load_state("networkidle")
        self.dashboard_heading.wait_for(state="visible")