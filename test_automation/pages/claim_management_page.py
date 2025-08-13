'''from playwright.sync_api import Page, expect

class ClaimManagementPage:
    def __init__(self, page: Page):
        self.page = page
        
        # Page elements
        self.page_heading = page.locator("h1:has-text('New Claim Submission')")
        
        # Filter and control elements - More flexible selectors
        self.payer_filter = page.locator("button:has-text('Payer')")
        self.status_filter = page.locator("button:has-text('Status')")
        self.date_filter = page.locator("//span[@class='truncate']")
        self.columns_filter = page.locator("button:has-text('Select Columns')")
        self.add_new_button = page.locator("button:has-text('Add New')")
        
        # Search elements
        self.search_box = page.locator("input[placeholder*='TID']")
        self.search_button = page.locator("button:has-text('Search')")
        
        # Grid elements - More flexible approach
        self.claims_grid = page.locator("[role='grid'], .ag-grid-wrapper, table")
        self.pagination_info = page.locator("text=/Showing.*entries/")
        self.entries_dropdown = page.locator("//select[@class='border border-gray-300 rounded px-2 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500']")
        
        # Payer options in dropdown
        self.maa_option = page.locator("button:has-text('MAA')")
        self.rghs_option = page.locator("button:has-text('RGHS')")
        
        # Claim form elements - More specific selectors
        self.form_heading = page.locator("//h2[normalize-space()='Create New Claim : MAA']")
        self.tid_field = page.locator("//input[@class='w-full border border-gray-300 rounded-md px-3 py-1']")
        self.stage_dropdown = page.locator("//select[@class='w-full border border-gray-300 rounded-md px-3 py-1 bg-white']")
        self.upload_area = page.locator("text=/Choose.*file.*drag/")
        self.choose_file_button = page.locator("(//div[contains(@class,'border-3 border-dashed border-[#CBD0DC] rounded-4xl p-6 flex flex-col items-center justify-center cursor-pointer hover:bg-gray-50')])[1]")
        self.submit_button = page.locator("button:has-text('Submit')")
        self.cancel_button = page.locator("button:has-text('Cancel')")

    def navigate_to_claims(self):
        """Navigate to claim management page"""
        self.page.goto("https://qa.eyther.ai/claims/hospital")
        self.page.wait_for_load_state("networkidle")

    def search_by_tid(self, tid: str):
        """Search for claim by TID"""
        self.search_box.fill(tid)
        self.search_button.click()
        self.page.wait_for_timeout(2000)

    def clear_search(self):
        """Clear search field"""
        self.search_box.clear()
        self.search_button.click()

    def open_add_new_dropdown(self):
        """Open Add New dropdown"""
        self.add_new_button.click()
        self.page.wait_for_timeout(1000)

    def select_payer_maa(self):
        """Select MAA payer option"""
        self.open_add_new_dropdown()
        self.maa_option.click()
        self.page.wait_for_timeout(2000)

    def select_payer_rghs(self):
        """Select RGHS payer option"""
        self.open_add_new_dropdown()
        self.rghs_option.click()
        self.page.wait_for_timeout(2000)

    def fill_tid_number(self, tid: str):
        """Fill TID number in form - Fixed strict mode violation"""
        # Use more specific selector for TID field in form
        tid_input = self.page.locator("div:has-text('TID Number') >> input[type='text']")
        tid_input.fill(tid)

    def select_stage(self, stage: str):
        """Select stage from dropdown - Fixed multiple elements issue"""
        # Target the stage dropdown specifically
        stage_select = self.page.locator("div:has-text('Stage') >> select")
        stage_select.select_option(stage)

    def submit_claim_form(self):
        """Submit claim form"""
        self.submit_button.click()

    def cancel_claim_form(self):
        """Cancel claim form"""
        self.cancel_button.click()

    def is_claims_page_loaded(self):
        """Check if claims page is loaded"""
        return self.page_heading.is_visible() and "/claims/hospital" in self.page.url

    def get_grid_data(self, column: str, row_index: int = 0):
        """Get data from grid by column name"""
        cell = self.page.locator(f"td:has-text('{column}')").first()
        return cell.inner_text() if cell.is_visible() else None

    def change_entries_per_page(self, entries: str):
        """Change number of entries per page"""
        # Target pagination dropdown specifically
        pagination_select = self.page.locator("div:has-text('Show:') >> select")
        pagination_select.select_option(entries)
        self.page.wait_for_timeout(1000)

    def wait_for_claims_load(self):
        """Wait for claims page to load completely"""
        self.page.wait_for_load_state("networkidle")
        self.page_heading.wait_for(state="visible", timeout=10000)'''


from playwright.sync_api import Page, expect

class ClaimManagementPage:
    def __init__(self, page: Page):
        self.page = page
        
        # Page elements
        self.page_heading = page.locator("h1:has-text('New Claim Submission')")
        
        # Filter and control elements - More flexible selectors
        self.payer_filter = page.locator("button:has-text('Payer')")
        self.status_filter = page.locator("button:has-text('Status')")
        self.date_filter = page.locator("//span[@class='truncate']")
        self.columns_filter = page.locator("button:has-text('Select Columns')")
        self.add_new_button = page.locator("button:has-text('Add New')")
        
        # Search elements
        self.search_box = page.locator("input[placeholder*='TID']")
        self.search_button = page.locator("button:has-text('Search')")
        
        # Grid elements - More flexible approach
        self.claims_grid = page.locator("[role='grid'], .ag-grid-wrapper, table").first
        self.pagination_info = page.locator("text=/Showing.*entries/")
        self.entries_dropdown = page.locator("//select[@class='border border-gray-300 rounded px-2 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500']")
        
        # Payer options in dropdown
        self.maa_option = page.locator("button:has-text('MAA')")
        self.rghs_option = page.locator("button:has-text('RGHS')")
        
        # Claim form elements - More specific selectors
        self.form_heading = page.locator("//h2[normalize-space()='Create New Claim : MAA']")
        self.tid_field = page.locator("//input[@class='w-full border border-gray-300 rounded-md px-3 py-1']")
        self.stage_dropdown = page.locator("//select[@class='w-full border border-gray-300 rounded-md px-3 py-1 bg-white']")
        self.upload_area = page.locator("text=/Choose.*file.*drag/")
        self.choose_file_button = page.locator("(//div[contains(@class,'border-3 border-dashed border-[#CBD0DC] rounded-4xl p-6 flex flex-col items-center justify-center cursor-pointer hover:bg-gray-50')])[1]")
        self.submit_button = page.locator("button:has-text('Submit')")
        self.cancel_button = page.locator("button:has-text('Cancel')")

    def navigate_to_claims(self):
        """Navigate to claim management page"""
        self.page.goto("https://qa.eyther.ai/claims/hospital")
        self.page.wait_for_load_state("networkidle")

    def search_by_tid(self, tid: str):
        """Search for claim by TID"""
        self.search_box.fill(tid)
        self.search_button.click()
        self.page.wait_for_timeout(2000)

    def clear_search(self):
        """Clear search field"""
        self.search_box.clear()
        self.search_button.click()

    def open_add_new_dropdown(self):
        """Open Add New dropdown"""
        self.add_new_button.click()
        self.page.wait_for_timeout(1000)

    def select_payer_maa(self):
        """Select MAA payer option"""
        self.open_add_new_dropdown()
        self.maa_option.click()
        self.page.wait_for_timeout(2000)

    def select_payer_rghs(self):
        """Select RGHS payer option"""
        self.open_add_new_dropdown()
        self.rghs_option.click()
        self.page.wait_for_timeout(2000)

    def fill_tid_number(self, tid: str):
        """Fill TID number in form - Fixed strict mode violation"""
        # Use more specific selector for the TID field in the form (not the search box)
        tid_input = self.page.locator("input.w-full.border.border-gray-300.rounded-md.px-3.py-1").nth(0)
        tid_input.fill(tid)

    def select_stage(self, stage: str):
        """Select stage from dropdown - Fixed multiple elements issue"""
        # Use more specific selector for the stage dropdown
        stage_select = self.page.locator("select.w-full.border.border-gray-300.rounded-md").nth(0)
        # Try to select by label first, then by value
        try:
            stage_select.select_option(label=stage)
        except:
            # If label doesn't work, try by value
            stage_value_map = {
                "Discharge": "SETTLEMENT",
                "Pre Auth": "PRE_AUTH",
                "SETTLEMENT": "SETTLEMENT",
                "PRE_AUTH": "PRE_AUTH"
            }
            value = stage_value_map.get(stage, stage)
            stage_select.select_option(value=value)

    def submit_claim_form(self):
        """Submit claim form"""
        self.submit_button.click()

    def cancel_claim_form(self):
        """Cancel claim form"""
        self.cancel_button.click()

    def is_claims_page_loaded(self):
        """Check if claims page is loaded"""
        return self.page_heading.is_visible() and "/claims/hospital" in self.page.url

    def get_grid_data(self, column: str, row_index: int = 0):
        """Get data from grid by column name"""
        cell = self.page.locator(f"td:has-text('{column}')").first
        return cell.inner_text() if cell.is_visible() else None

    def change_entries_per_page(self, entries: str):
        """Change number of entries per page"""
        # Target pagination dropdown specifically - use nth to avoid strict mode
        pagination_select = self.page.locator("div:has-text('Show:') >> select").nth(0)
        pagination_select.select_option(entries)
        self.page.wait_for_timeout(1000)

    def wait_for_claims_load(self):
        """Wait for claims page to load completely"""
        self.page.wait_for_load_state("networkidle")
        self.page_heading.wait_for(state="visible", timeout=10000)