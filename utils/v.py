import os
import time
import shutil
import tempfile
import datetime
import win32com.client as win32
from config_paths import get_wt_paths

def clear_gen_py_cache():
    gen_py_dir = os.path.join(tempfile.gettempdir(), "gen_py")
    if os.path.exists(gen_py_dir):
        try:
            shutil.rmtree(gen_py_dir)
            print(f"🧹 Cleared COM cache: {gen_py_dir}")
        except Exception as e:
            print(f"⚠️ Failed to delete {gen_py_dir}: {e}")
    else:
        print(f"ℹ️ gen_py folder not found at: {gen_py_dir}")

def open_excel():
    paths = get_wt_paths()

    file1 = paths["new_order_file"]
    file2 = paths["old_order_file"]
    xlsx_path = paths["core_2_1"]
    target_sheet = "BW出库一遍过"

    today = datetime.date.today()

    def is_modified_today(path: str) -> bool:
        return os.path.isfile(path) and datetime.datetime.fromtimestamp(os.path.getmtime(path)).date() == today

    if is_modified_today(file1) and is_modified_today(file2):
        try:
            excel = win32.Dispatch("Excel.Application")
            excel.Visible = True
            wb = excel.Workbooks.Open(xlsx_path)

            # active sheet
            wb.Sheets(target_sheet).Activate()

        except Exception as e:
            print(f"❌ Operation failed: {e}")
    else:
        print("📌 One or both order files are not updated today. Skipping Excel launch.")

def excel_process():
    clear_gen_py_cache()

    time.sleep(1)
    
    open_excel()

'''
if __name__ == "__main__":
    excel_process()
'''