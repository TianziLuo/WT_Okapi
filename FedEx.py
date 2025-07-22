from playwright.sync_api import sync_playwright
import time

from playwright.sync_api import sync_playwright

USERNAME = "Acolortree168"
PASSWORD = "Colourtree168!"
FILE_PATH = r"C:\Template\pickup_template.xlsx"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # 打开登录页
    page.goto("https://www.fedex.com/PickupApp/login?locale=en_US")

    # 等待用户名输入框出现并填写
    page.wait_for_selector('input#username', timeout=15000)
    page.fill('input#username', USERNAME)

    # 等待密码框并填写（通常是 input[type="password"]）
    page.wait_for_selector('input[type="password"]', timeout=10000)
    page.fill('input[type="password"]', PASSWORD)

    # 点击 Sign In 按钮
    page.click('button:has-text("LOG IN")')

    # 可选：等待跳转或登录成功
    page.wait_for_load_state("networkidle")

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