from playwright.sync_api import sync_playwright

def uni():
    EMAIL = "colourtreeusa@gmail.com"
    PASSWORD = "Colourtree168!"
    FILE_PATH = r"C:\Template\pickup_template.xlsx"  

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 打开登录页
        page.goto("https://prm.uniuni.com/main")

        # 登录流程
        page.wait_for_selector('input[type="text"]')
        page.locator('input[type="text"]').fill(EMAIL)
        page.locator('input[type="password"]').fill(PASSWORD)
        page.locator('button:has-text("Sign In")').click()

        # 等待页面跳转后点击菜单
        page.wait_for_selector("text=Schedule Pickup", timeout=10000)
        page.click("text=Schedule Pickup")
        page.wait_for_selector("text=Batch Upload", timeout=10000)
        page.click("text=Batch Upload")

        # ⏳ 等上传组件加载（调整等待时间或用选择器）
        page.wait_for_timeout(3000)

        # 查找 file input 元素（type="file"）并上传文件
        file_input = page.locator('input[type="file"]')
        file_input.set_input_files(FILE_PATH)

        
        input("✅ 文件已上传，按 Enter 结束脚本...")

        browser.close()