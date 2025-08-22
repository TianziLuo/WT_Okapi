import os
from pathlib import Path
from utils.copy_file import latest_matching_file, copy_file


def copy_from_downloads():
    source = Path(os.path.expanduser("~/Downloads"))
    target = Path(r"C:\ACT\公用核心\每天自发货")
    keywords = ["Use"]

    for kw in keywords:
        latest = latest_matching_file(source, [".csv"], [kw], only_today=True)
        if latest:
            copy_file(latest, target)
        else:
            print(f"⚠️ No CSV file containing '{kw}' found for today")


'''
if __name__ == "__main__":
    copy_from_downloads()
'''