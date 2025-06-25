import os
import shutil
import time
from datetime import datetime
from pathlib import Path
import pygetwindow as gw

# Utility function: find the latest file matching extension and keywords
def latest_matching_file(folder: Path, extensions, keywords, only_today=False):
    latest, latest_mtime = None, 0
    today = datetime.today().date()

    for root, _, files in os.walk(folder):
        for fname in files:
            if not any(fname.endswith(ext) for ext in extensions):
                continue
            if not any(kw in fname for kw in keywords):
                continue

            fpath = Path(root) / fname
            mtime = fpath.stat().st_mtime
            if only_today and datetime.fromtimestamp(mtime).date() != today:
                continue
            if mtime > latest_mtime:
                latest, latest_mtime = fpath, mtime
    return latest

# Utility function: copy file to target directory
def copy_file(src: Path, dst_dir: Path):
    dst = dst_dir / src.name
    shutil.copy2(src, dst)
    print(f"✅ Copied: {src.name} → {dst_dir}")

# Utility function: close Windows Explorer window by folder name
def close_explorer_window():
    time.sleep(2)
    folder_name = "无小票发货 Sarah"  # Folder window title in Explorer
    for window in gw.getWindowsWithTitle(folder_name):
        if window.visible:
            window.close()
            print(f"✅ Closed Explorer window: {window.title}")
            break
