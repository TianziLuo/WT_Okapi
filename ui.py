import tkinter as tk
import sys
from console import ConsoleRedirector
from threaded import threaded
from handlers.tp_download import run_download_tp
from handlers.actions import ACTIONS
from TP_acc import ACCOUNTS

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("🦫 WT Okapi - Capybara Edition")
        self.root.geometry("475x530")
        self.root.configure(bg="#e9ede2")
        self.checkbox_vars = []

        self.build_ui()
        self.build_console()

        sys.stdout = ConsoleRedirector(self.console)
        sys.stderr = ConsoleRedirector(self.console)

    def build_ui(self):
        self.add_title()
        row = 1
        row = self.add_download_section(row)  # TP Download move to the second line
        for label, func in ACTIONS:
            row = self.add_button_row(label, func, row)

    def add_title(self):
        tk.Label(
            self.root,
            text="🦫 WT Okapi",
            font=('Segoe UI', 20, 'bold'),
            bg="#e9ede2",
            fg="#5a4a3c",
            anchor="center",  
            justify="center"
        ).grid(row=0, column=0, columnspan=3, pady=15, sticky="nsew")  

    def add_button_row(self, label, func, row):
        tk.Label(
            self.root,
            text=label,
            font=('Segoe UI', 12, 'bold'),
            bg="#e9ede2",
            fg="#4a4038"
        ).grid(row=row, column=0, sticky='w', padx=10, pady=5)

        tk.Button(
            self.root,
            text="Run",
            command=threaded(func),
            bg="#9E6C55",
            fg="#fdf8f4",
            font=('Segoe UI', 12, 'bold'),
            width=12,
            relief="flat",
            bd=0
        ).grid(row=row, column=1, pady=5)
        return row + 1

    def add_download_section(self, start_row):
        row = start_row
        tk.Label(
            self.root,
            text="• Download TP Orders:",
            font=('Segoe UI', 12, 'bold'),
            bg="#e9ede2",
            fg="#4a4038"
        ).grid(row=row, column=0, sticky='w', padx=15, pady=10)

        tk.Button(
            self.root,
            text="Download",
            command=lambda: run_download_tp(self.checkbox_vars),
            bg="#9E6C55",
            fg="#fdf8f4",
            font=('Segoe UI', 12, 'bold'),
            width=12,
            relief="flat",
            bd=0
        ).grid(row=row, column=1, sticky='e', padx=15, pady=10)

        row += 1
        for acct in ACCOUNTS:
            var = tk.BooleanVar()
            tk.Checkbutton(
                self.root,
                text=acct["USERNAME"],
                variable=var,
                bg="#e9ede2",
                font=('Segoe UI', 11, 'bold'),
                fg="#4a4038",
                selectcolor="#e9ede2"
            ).grid(row=row, column=0, sticky='w', padx=30)
            self.checkbox_vars.append((var, acct))
            row += 1
        return row

    def build_console(self):
        tk.Label(
            self.root,
            text="Console Output:",
            font=('Segoe UI', 14, 'bold'),
            bg="#e9ede2",
            fg="#4a4038"
        ).grid(row=1000, column=0, columnspan=3, sticky='w', padx=15, pady=(10, 0))  

        self.console = tk.Text(
            self.root,
            height=10,
            width=50,
            bg="#fdf8f4",
            fg="#3e3e3e",
            font=('Consolas', 10),
            wrap='word',
            relief="solid",
            bd=1
        )
        self.console.grid(row=1001, column=0, columnspan=3, padx=15, pady=10, sticky='nsew')

        self.root.grid_rowconfigure(1001, weight=1)
        self.root.grid_columnconfigure(0, weight=1)