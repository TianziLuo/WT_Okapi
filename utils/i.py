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
    # 第一组路径和关键词
    target1 = Path(r"C:\Frank\易仓-TP\无小票发货 Sarah")
    keywords1 = ["新范本", "店小秘 非BW", "店小秘 BW"]
    clean_folder(target1)
    time.sleep(1)
    copy_wechat_files(target1, keywords1)

    # 第二组路径和关键词
    target2 = Path(r"C:\ACT\数据对接Frank\每日自发货文件")
    keywords2 = ["发货小票", "店小秘 非BW"]
    copy_wechat_files(target2, keywords2)

    os.startfile(target1)
    os.startfile(target2)

'''
if __name__ == "__main__":
    clean_folder_and_copy_files()
'''
