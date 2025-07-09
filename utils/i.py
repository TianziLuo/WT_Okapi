import os
import time
from pathlib import Path
from datetime import datetime
from send2trash import send2trash
from utils.copy_file import latest_matching_file, copy_file 
def clean_folder(folder_path: Path):
    file_patterns = ['*.xlsx', '*.csv']
    files_to_delete = []
    for pattern in file_patterns:
        files_to_delete.extend(folder_path.glob(pattern))  

    for file in files_to_delete:
        try:
            send2trash(str(file))
            print(f"🗑️ Moved to Recycle Bin: {file}")
        except Exception as e:
            print(f"❌ Failed to delete: {file}, Reason: {e}")

def copy_wechat_files(target: Path):
    month = datetime.now().strftime("%Y-%m")
    source = Path(fr"C:\Users\monica\Documents\xwechat_files\qingchen536521_c584\msg\file\{month}")
    keywords = ["新范本", "店小秘 非BW", "店小秘 BW"]

    for kw in keywords:
        latest = latest_matching_file(source, [".xlsx"], [kw], only_today=False)
        if latest:
            copy_file(latest, target)
            print(f"✅ Copied file with keyword '{kw}': {latest}")
        else:
            print(f"⚠️ No Excel file found with keyword '{kw}'")

def clean_folder_and_copy_files():
    target_folder = Path(r"C:\Frank\易仓-TP\无小票发货 Sarah")

    clean_folder(target_folder)

    time.sleep(1)

    copy_wechat_files(target_folder)

    os.startfile(target_folder)

'''
if __name__ == "__main__":
    clean_folder_and_copy_files()
'''
