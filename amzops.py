import tkinter as tk
import subprocess
from threaded import threaded 
import os   

@threaded
def run_go_exe():
    exe_path = os.path.join(os.path.dirname(__file__), "amzfileops.exe")
    source = r"C:\ACT\RPA自动下载\AMZ_12345"
    target = r"C:\ACT\公用核心\Amazon\下载_2.1 AMZ日报"

    result = subprocess.run(
        [exe_path, source, target],
        capture_output=True,
        text=True
    )
    print("Go Output:\n", result.stdout)
    if result.stderr:
        print("Go Error:\n", result.stderr)