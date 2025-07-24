import threading
import traceback
from tkinter import messagebox

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
                messagebox.showerror("Error", f"❌ {fn.__name__} failed.\nSee console for details.")
        threading.Thread(target=run_and_report, daemon=True).start()
    return wrapper
