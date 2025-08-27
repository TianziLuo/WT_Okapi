import subprocess
import os
import sys
from threaded import threaded

def resource_path(relative_path):
    # Get absolute path to a resource.
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)

@threaded
def run_go_exe():
    exe_path = resource_path("amzfileops.exe")
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