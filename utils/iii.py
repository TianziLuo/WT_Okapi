import time
from pathlib import Path
from playwright.sync_api import sync_playwright
from config_paths import get_wt_paths

def detect_login_placeholders(page):
    """Detect login form placeholders using keyword matching"""
    # Get all input placeholders on the page
    placeholders = []
    try:
        inputs = page.locator('input[placeholder]')
        for i in range(inputs.count()):
            placeholder = inputs.nth(i).get_attribute('placeholder')
            if placeholder:
                placeholders.append(placeholder)
    except:
        pass
    
    print(f"🔍 Found placeholders: {placeholders}")
    
    # Keyword matching for different field types
    username_keywords = ['账户', '用户', 'account', 'login', '邮箱', 'email']
    email_keywords = ['邮件', 'email', 'mail', '电子']
    password_keywords = ['密码', 'password', 'pass']
    
    # Find fields by keyword matching
    username_placeholder = None
    email_placeholder = None
    password_placeholder = None
    
    for placeholder in placeholders:
        placeholder_lower = placeholder.lower()
        
        # Check for username field
        if not username_placeholder:
            for keyword in username_keywords:
                if keyword in placeholder_lower:
                    username_placeholder = placeholder
                    break
        
        # Check for email field
        if not email_placeholder:
            for keyword in email_keywords:
                if keyword in placeholder_lower:
                    email_placeholder = placeholder
                    break
        
        # Check for password field
        if not password_placeholder:
            for keyword in password_keywords:
                if keyword in placeholder_lower:
                    password_placeholder = placeholder
                    break
    
    return username_placeholder, email_placeholder, password_placeholder

def download_TP(USERNAME: str, EMAIL: str, PASSWORD: str, FILENAME: str,
                chrome_path: str = r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                headless: bool = False) -> None:
    
    paths = get_wt_paths()
    target_folder = paths["tp_download_folder"]

    file_path = Path(target_folder) / FILENAME
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=chrome_path,
                                    headless=headless)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        # Login
        page.goto("https://www.teapplix.com/auth/")
        
        # Detect placeholders dynamically
        username_placeholder, email_placeholder, password_placeholder = detect_login_placeholders(page)
        
        print(f"🔍 Detected placeholders - Username: {username_placeholder}, Email: {email_placeholder}, Password: {password_placeholder}")
        
        # Fill login form with detected placeholders
        if username_placeholder:
            page.fill(f'input[placeholder="{username_placeholder}"]', USERNAME)
        else:
            # Fallback to first text input
            page.locator('input[type="text"]').first.fill(USERNAME)
            
        if email_placeholder:
            page.fill(f'input[placeholder="{email_placeholder}"]', EMAIL)
        else:
            # Fallback to email input or second text input
            try:
                page.locator('input[type="email"]').first.fill(EMAIL)
            except:
                page.locator('input[type="text"]').nth(1).fill(EMAIL)
                
        if password_placeholder:
            page.fill(f'input[placeholder="{password_placeholder}"]', PASSWORD)
        else:
            # Fallback to password input
            page.locator('input[type="password"]').first.fill(PASSWORD)

        page.click('button.ant-btn-primary')
        page.wait_for_load_state("networkidle")
        print("✅ Login successful")

        # Go to reports
        page.wait_for_selector("text=Reports", timeout=10000)
        page.click("text=Reports")
        page.wait_for_selector("text=Order Report", timeout=10000)
        page.click("text=Order Report")
        print("✅ Entered Order Report page")

        # Select "shipped", unselect "open"
        page.locator('input.ant-checkbox-input[value="open"]').uncheck()
        page.locator('input.ant-checkbox-input[value="shipped"]').check()
        time.sleep(10)

        # Export CSV
        page.wait_for_selector("text=One line per order item", timeout=10000)
        page.click("text=One line per order item")

        with page.expect_download() as download_info:
            page.click("text=Export to CSV")
        download = download_info.value
        download.save_as(file_path)
        print(f"✅ File saved and overwritten: {file_path}")

        # Close browser
        browser.close()

'''
if __name__ == "__main__":

    ACCOUNTS = [
        {
            "USERNAME": "wayfaircolourtree",
            "EMAIL": "wayfair.colourtree@gmail.com",
            "PASSWORD": "Colourtree168!!",
            "FILENAME": "新TP订单下载 order_report.csv"
        },
        {
            "USERNAME" : "colourtree",
            "EMAIL" : "colourtreeusa@gmail.com",
            "PASSWORD" : "Colourtree168!",
            "FILENAME": "老TP订单下载 order_report.csv"
        }
    ]

    for acct in ACCOUNTS:
        print(f"\n▶▶ 开始处理账号：{acct['USERNAME']}")
        download_TP(
            USERNAME=acct["USERNAME"],
            EMAIL=acct["EMAIL"],
            PASSWORD=acct["PASSWORD"],
            FILENAME=acct["FILENAME"],
            headless=False)                    

        print(f"⏳ {acct['USERNAME']} 完成，准备切换下一个账号 …\n")
        time.sleep(2) 
'''