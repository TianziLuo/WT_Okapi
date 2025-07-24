from TP_acc import ACCOUNTS
from utils.func import download_TP
from tkinter import messagebox
from threaded import threaded

@threaded
def run_download_tp(checkbox_vars):
    failed_accounts = []
    for var, acct in checkbox_vars:
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
        messagebox.showerror("Error", f"❌ Failed accounts:\n" + "\n".join(failed_accounts))
