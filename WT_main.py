import tkinter as tk
from tkinter import messagebox
from ui import App
from verify import verify_license
import sys


if __name__ == "__main__":
    ok, msg = verify_license()
    if not ok:
        messagebox.showerror("License fail", msg)
        sys.exit()

    # main loop
    root = tk.Tk()
    app = App(root)
    root.mainloop()
