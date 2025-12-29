import tkinter as tk
from tkinter import messagebox
from ui import App
from verify import verify_license
import sys
import threading

def _start_api_server():
    try:
        import uvicorn
        from api import app as fastapi_app
        # Run Uvicorn server; host 127.0.0.1, port 8000
        uvicorn.run(fastapi_app, host="127.0.0.1", port=8000, log_level="info")
    except Exception as e:
        # Avoid crashing GUI if API fails to start
        print(f"Failed to start API server: {e}")


if __name__ == "__main__":
    ok, msg = verify_license()
    if not ok:
        messagebox.showerror("License fail", msg)
        sys.exit()

    # Start FastAPI server in background
    threading.Thread(target=_start_api_server, daemon=True).start()

    # main loop
    root = tk.Tk()
    app = App(root)
    root.mainloop()
