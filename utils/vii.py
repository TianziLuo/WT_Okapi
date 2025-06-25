import os
from pathlib import Path
from utils.copy_file import latest_matching_file, copy_file, close_explorer_window


def copy_from_downloads():
    source = Path(os.path.expanduser("~/Downloads"))
    target = Path(r"C:\Frank\易仓-TP\无小票发货 Sarah")
    keywords = ["Use"]

    for kw in keywords:
        latest = latest_matching_file(source, [".csv"], [kw], only_today=True)
        if latest:
            copy_file(latest, target)
        else:
            print(f"⚠️ 未找到今天包含「{kw}」的 CSV 文件")

    close_explorer_window()

'''
if __name__ == "__main__":
    copy_from_downloads()
'''