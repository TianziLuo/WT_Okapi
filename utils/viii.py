import os
import sys 
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from config_paths import get_wt_paths

def copy2downloads():
    paths = get_wt_paths()
    
    # —————— Configuration ——————
    source_path = paths["core_2_1"]
    download_dir = paths["downloads"]
    max_file_age = 30 

    # 1) Check that the source file exists
    if not Path(source_path).is_file():
        sys.exit(f"❌ Source file not found: {source_path}")

    # 2) Verify the file’s last‑modified time
    mtime = datetime.fromtimestamp(os.path.getmtime(source_path))
    now   = datetime.now()

    if now - mtime > timedelta(seconds = max_file_age):
        seconds_ago = int((now - mtime).total_seconds())
        sys.exit(
            f"⚠️ Last saved {seconds_ago} seconds ago, "
            f"exceeding the {max_file_age}‑second limit; copy aborted."
        )

    # 3) Build the destination filename
    date_str  = now.strftime('%m%d')         
    stem      = Path(source_path).stem        
    extension = Path(source_path).suffix       
    new_name  = f"{stem} {date_str}{extension}"
    dest_path = download_dir / new_name

    # 4) Perform the copy
    shutil.copy2(source_path, dest_path)

    print(f"✅ File copied to: {dest_path}")

'''
if __name__ == "__main__":
    copy2downloads()
'''