from playwright.sync_api import sync_playwright

def uni():
    EMAIL = "colourtreeusa@gmail.com"
    PASSWORD = "Colourtree168!"
    FILE_PATH = r"C:\Template\pickup_template.xlsx"  

    chrome_path: str = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    headless: bool = False
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=chrome_path,
                                    headless=headless)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        # Go to login page
        page.goto("https://prm.uniuni.com/main")

        # LOGIN
        page.wait_for_selector('input[type="text"]')
        page.locator('input[type="text"]').fill(EMAIL)
        page.locator('input[type="password"]').fill(PASSWORD)
        page.locator('button:has-text("Sign In")').click()

        # options
        page.wait_for_selector("text=Schedule Pickup", timeout=10000)
        page.click("text=Schedule Pickup")
        page.wait_for_selector("text=Batch Upload", timeout=10000)
        page.click("text=Batch Upload")

        # Wait for upload
        page.wait_for_timeout(3000)

        # Find file input element
        file_input = page.locator('input[type="file"]')
        file_input.set_input_files(FILE_PATH)

        input("✅ File uploaded. Press Enter to exit the script...")

        browser.close()
