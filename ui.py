# ui.py
import tkinter as tk
import threading
import traceback
from TP_acc import ACCOUNTS
from tkinter import messagebox
from utils.func import (
    clean_folder,
    copy_weChat_files,
    download_TP,
    clear_gen_py_cache,
    open_excel,
    WT_out,
    copy_from_downloads,
    copy2downloads
)

def threaded(fn):
    def wrapper(*args, **kwargs):
        def run_and_report():
            try:
                fn(*args, **kwargs)
                print(f"✅ {fn.__name__} succeeded.")
                messagebox.showinfo("Success", "✅ Operation completed.")
            except Exception as e:
                print(f"❌ Error in {fn.__name__}: {e}")
                print(traceback.format_exc())
                messagebox.showerror("Error", f"❌ {fn.__name__} failed.\nSee terminal for details.")
        threading.Thread(target=run_and_report, daemon=True).start()
    return wrapper

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("🦫 WT Okapi - Capybara Edition")
        self.root.geometry("430x530")
        self.root.configure(bg="#e9ede2")  # Capybara background
        self.checkbox_vars = []
        self.build_ui()

    def build_ui(self):
        self.add_title()
        row = 1
        row = self.add_button_row("Clean Sarah Folder", clean_folder, row)
        row = self.add_button_row("Copy WeChat Files", copy_weChat_files, row)
        row = self.add_download_section(row)
        row = self.add_button_row("Clear Cache", clear_gen_py_cache, row)
        row = self.add_button_row("Open 2.1", open_excel, row)
        row = self.add_button_row("WT Outbound", WT_out, row)
        row = self.add_button_row("Copy 'Use' from Downloads", copy_from_downloads, row)
        row = self.add_button_row("Copy 2.1 to Downloads", copy2downloads, row)

    def add_title(self):
        tk.Label(
            self.root,
            text="🦫 WT Okapi",
            font=('Segoe UI', 20, 'bold'),
            bg="#e9ede2",
            fg="#5a4a3c"
        ).grid(row=0, column=0, columnspan=3, pady=15)

    def add_button_row(self, label, func, row):
        tk.Label(
            self.root,
            text=label,
            font=('Segoe UI', 12, 'bold'),
            bg="#e9ede2",
            fg="#4a4a4a"
        ).grid(row=row, column=0, sticky='w', padx=10, pady=5)

        tk.Button(
            self.root,
            text="Run",
            command=threaded(func),
            bg="#8e735b",
            fg="#fffaf0",
            font=('Segoe UI', 12, 'bold'),
            width=12,
            height=1,
            activebackground="#a89b94",
            activeforeground="#ffffff"
        ).grid(row=row, column=1, pady=5)
        return row + 1

    def add_download_section(self, start_row):
        row = start_row
        tk.Label(
            self.root,
            text="Download TP Orders:",
            font=('Segoe UI', 12, 'bold'),
            bg="#e9ede2",
            fg="#4a4a4a"
        ).grid(row=row, column=0, sticky='w', padx=15, pady=10)

        tk.Button(
            self.root,
            text="Download",
            command=self.run_download_tp,
            bg="#8e735b",
            fg="#fffaf0",
            font=('Segoe UI', 12, 'bold'),
            width=12,
            height=1,
            activebackground="#a89b94",
            activeforeground="#ffffff"
        ).grid(row=row, column=1, sticky='e', padx=15, pady=10)

        row += 1
        for acct in ACCOUNTS:
            var = tk.BooleanVar()
            cb = tk.Checkbutton(
                self.root,
                text=acct["USERNAME"],
                variable=var,
                bg="#e9ede2",
                font=('Segoe UI', 11,'bold'),
                fg="#3e3e3e",
                activebackground="#e9ede2",
                activeforeground="#3e3e3e",
                selectcolor="#e9ede2"
            )
            cb.grid(row=row, column=0, sticky='w', padx=30)
            self.checkbox_vars.append((var, acct))
            row += 1
        return row

    @threaded
    def run_download_tp(self):
        failed_accounts = []

        for var, acct in self.checkbox_vars:
            if var.get():
                try:
                    print(f"▶▶ Processing account: {acct['USERNAME']}")
                    download_TP(
                        USERNAME=acct["USERNAME"],
                        EMAIL=acct["EMAIL"],
                        PASSWORD=acct["PASSWORD"],
                        FILENAME=acct["FILENAME"],
                        headless=False
                    )
                except Exception as e:
                    print(f"❌ Failed for {acct['USERNAME']}: {e}")
                    failed_accounts.append(acct["USERNAME"])

        if not failed_accounts:
            messagebox.showinfo("Success", "✅ All accounts downloaded successfully.")
        else:
            failed_str = "\n".join(failed_accounts)
            messagebox.showerror("Error", f"❌ Failed accounts:\n{failed_str}\nSee terminal for details.")