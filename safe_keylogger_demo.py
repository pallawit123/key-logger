# safe_keylogger_demo.py
# Demo: captures keys typed into this app window only. For learning only.
import tkinter as tk
import sys
from datetime import datetime, timezone
from pathlib import Path

LOG_FILE = Path("keystrokes_demo.log")

class DemoLogger:
    def __init__(self, root):
        self.root = root
        root.title("Safe Keystroke Capture Demo (Window-Limited)")
        self.text = tk.Text(root, width=80, height=20)
        self.text.pack(padx=8, pady=8)
        self.logging = False

        ctrl_frame = tk.Frame(root)
        ctrl_frame.pack(fill="x", padx=8)
        self.btn = tk.Button(ctrl_frame, text="Start Logging", command=self.toggle)
        self.btn.pack(side="left")
        self.status = tk.Label(ctrl_frame, text="Logging: OFF")
        self.status.pack(side="left", padx=8)
        self.info = tk.Label(root, text=f"Logging to: {LOG_FILE.resolve()}")
        self.info.pack(anchor="w", padx=8, pady=(0,8))

        # Bind key event only for this widget
        self.text.bind("<Key>", self.on_key)

    def toggle(self):
        self.logging = not self.logging
        self.btn.config(text="Stop Logging" if self.logging else "Start Logging")
        self.status.config(text=f"Logging: {'ON' if self.logging else 'OFF'}")

    def on_key(self, event):
        # Only log when logging is active and the event originates in this widget
        if not self.logging:
            return
        # ensure the event comes from our text widget
        if event.widget is not self.text:
            return
        key = event.keysym
        char = event.char if event.char not in ("\x08", "\r", "") else ""
        # timezone-aware UTC timestamp without microseconds
        timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        entry = f"{timestamp}\tkeysym={key}\tchar={repr(char)}\n"
        try:
            LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
            with LOG_FILE.open("a", encoding="utf-8") as f:
                f.write(entry)
        except Exception as e:
            print(f"Failed to write log: {e}", file=sys.stderr)

if __name__ == "__main__":
    root = tk.Tk()
    DemoLogger(root)
    root.mainloop()