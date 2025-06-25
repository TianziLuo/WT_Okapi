import time
from pathlib import Path
from playwright.sync_api import sync_playwright

def download_TP(USERNAME: str, EMAIL: str, PASSWORD: str, FILENAME: str,
                target_folder: str = r"C:\Frank\原始数据\店小秘+TP+订单+盘点",
                chrome_path: str = r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                headless: bool = False) -> None:

    file_path = Path(target_folder) / FILENAME
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=chrome_path,
                                    headless=headless)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        # Login
        page.goto("https://www.teapplix.com/auth/")
        page.fill('input[placeholder="账户名"]', USERNAME)
        page.fill('input[placeholder="登录电子邮件"]', EMAIL)
        page.fill('input[placeholder="密码"]', PASSWORD)

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