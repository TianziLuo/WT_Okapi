from pathlib import Path
from utils.copy_file import latest_matching_file, copy_file
from datetime import datetime

def copy_weChat_files():
    month = datetime.now().strftime("%Y-%m")
    source = Path(fr"C:\Users\monica\Documents\xwechat_files\qingchen536521_c584\msg\file\{month}")
    target = Path(r"C:\Frank\易仓-TP\无小票发货 Sarah")
    keywords = ["新范本", "店小秘 非BW", "店小秘 BW"]

    for kw in keywords:
        latest = latest_matching_file(source, [".xlsx"], [kw], only_today=False)
        if latest:
            copy_file(latest, target)
        else:
            print(f"⚠️ 未找到包含「{kw}」的 Excel 文件")


'''
if __name__ == "__main__":
    copy_weChat_files()
    print
'''