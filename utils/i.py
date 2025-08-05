import os
import time
from pathlib import Path
from datetime import datetime
from send2trash import send2trash
from utils.copy_file import latest_matching_file, copy_file 

import shutil
from pathlib import Path

def clean_folder(folder_path: Path, target_folder: Path):
    file_patterns = ['*.xlsx', '*.csv']
    files_to_move = []

    for pattern in file_patterns:
        files_to_move.extend(folder_path.glob(pattern))

    for file in files_to_move:
        try:
            destination = target_folder / file.name
            shutil.move(str(file), str(destination))
            print(f"📁 Moved to: {destination}")
        except Exception as e:
            print(f"❌ Failed to move: {file}, Reason: {e}")

def copy_wechat_files(target: Path, keywords: list[str]):
    month = datetime.now().strftime("%Y-%m")
    source = Path(fr"C:\Users\monica\Documents\xwechat_files\qingchen536521_c584\msg\file\{month}")

    for kw in keywords:
        latest = latest_matching_file(source, [".xlsx"], [kw], only_today=False)
        if latest:
            copy_file(latest, target)
            print(f"✅ Copied file with keyword '{kw}': {latest}")
        else:
            print(f"⚠️ No Excel file found with keyword '{kw}'")

def clean_folder_and_copy_files():
    # BW
    target1 = Path(r"C:\Frank\易仓-TP\无小票发货 Sarah")
    folder1 = Path(r"C:\Frank\易仓-TP\无小票发货 Sarah\不要删除")
    keywords1 = ["TP", "店小秘 BW"]
    clean_folder(target1,folder1)
    time.sleep(1)
    copy_wechat_files(target1, keywords1)

    # DV
    target2 = Path(r"C:\ACT\数据对接Frank\每日自发货文件")
    folder2 = Path(r"C:\ACT\数据对接Frank\每日自发货文件\历史文件")
    keywords2 = ["发货小票", "店小秘 非BW"]
    clean_folder(target2,folder2)
    time.sleep(1)
    copy_wechat_files(target2, keywords2)

    os.startfile(target1)
    os.startfile(target2)

'''
if __name__ == "__main__":
    clean_folder_and_copy_files()
'''
