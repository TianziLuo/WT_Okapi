import os
import win32com.client

def create_shortcut(exe_path, shortcut_name="WT Okapi", icon_path=None):
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    path = os.path.join(desktop, f"{shortcut_name}.lnk")

    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(path)
    shortcut.TargetPath = exe_path
    shortcut.WorkingDirectory = os.path.dirname(exe_path)
    if icon_path:
        shortcut.IconLocation = icon_path
    shortcut.save()