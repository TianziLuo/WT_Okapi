import os
from pathlib import Path
from utils.copy_file import latest_matching_file, copy_file
from config_paths import get_wt_paths

def copy_from_downloads():
    paths = get_wt_paths()

    source = paths["downloads"]
    target = paths["shipping_folder"]
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