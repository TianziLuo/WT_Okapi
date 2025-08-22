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
    # BW DV
    target = Path(r"C:\ACT\公用核心\每天自发货")
    folder = Path(r"C:\ACT\公用核心\每天自发货\历史文件")
    keywords = ["发货小票", "店小秘 非BW","TP", "店小秘 BW"]
    clean_folder(target,folder)
    time.sleep(1)
    copy_wechat_files(target, keywords)

    os.startfile(target)

'''
if __name__ == "__main__":
    clean_folder_and_copy_files()
'''
