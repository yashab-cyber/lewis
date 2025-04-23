import tkinter as tk
from tkinter import messagebox, scrolledtext
import os
from pathlib import Path
import subprocess

CONFIG_PATH = Path.home() / ".lewis_config"
CONFIG_FILE = CONFIG_PATH / "preferences.cfg"

class FirstTimeSetup:
    def __init__(self, root):
        self.root = root
        self.root.title("LEWIS - First Time Setup")
        self.root.geometry("540x460")
        self.root.configure(bg="#101010")

        tk.Label(root, text="Welcome to LEWIS", font=("Helvetica", 18, "bold"), fg="#00ffd5", bg="#101010").pack(pady=15)
        tk.Label(root, text="Let's get your cybersecurity assistant ready", font=("Helvetica", 12), fg="#ccc", bg="#101010").pack(pady=5)

        self.steps = [
            "✓ Install dependencies",
            "✓ Configure LEWIS database",
            "✓ Setup AI & tools environment",
            "✓ Create application shortcut",
        ]
        for step in self.steps:
            tk.Label(root, text=step, font=("Helvetica", 10), fg="#00ff99", bg="#101010").pack(anchor="w", padx=40, pady=1)

        self.agree_var = tk.IntVar()
        tk.Checkbutton(root,
                       text="I agree to the Terms & Conditions and Privacy Policy",
                       variable=self.agree_var,
                       bg="#101010", fg="#ccc",
                       font=("Helvetica", 10),
                       selectcolor="#101010",
                       activebackground="#101010",
                       activeforeground="#00ffd5").pack(pady=10)

        self.skip_var = tk.IntVar()
        tk.Checkbutton(root,
                       text="Don't show this again",
                       variable=self.skip_var,
                       bg="#101010", fg="#999",
                       font=("Helvetica", 9),
                       selectcolor="#101010").pack(pady=5)

        button_frame = tk.Frame(root, bg="#101010")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Privacy Policy", command=self.show_policy,
                  bg="#222", fg="#00ffd5").grid(row=0, column=0, padx=10)

        tk.Button(button_frame, text="Start LEWIS", command=self.launch_lewis,
                  bg="#00ffd5", fg="#000").grid(row=0, column=1, padx=10)

    def show_policy(self):
        policy = tk.Toplevel(self.root)
        policy.title("Privacy Policy & Terms")
        policy.geometry("480x400")
        policy.configure(bg="#101010")

        text = scrolledtext.ScrolledText(policy, wrap=tk.WORD,
                                         fg="#ccc", bg="#101010", font=("Helvetica", 10))
        text.insert(tk.END, "LEWIS is a cybersecurity tool designed to help ethical hackers and security analysts...\n\n"
                            "Privacy Policy:\nLEWIS does not share or store your personal data.\n\n"
                            "Terms:\nYou must use this software only for ethical and legal purposes.\n"
                            "The creators are not responsible for misuse or damage caused by LEWIS.\n\n"
                            "© 2025 Zehra Sec. All rights reserved.")
        text.config(state=tk.DISABLED)
        text.pack(expand=True, fill='both', padx=10, pady=10)

    def launch_lewis(self):
        if not self.agree_var.get():
            messagebox.showwarning("Agreement Required", "You must agree to the terms and privacy policy to continue.")
            return

        CONFIG_PATH.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, "w") as f:
            f.write(f"skip_intro={bool(self.skip_var.get())}\n")

        try:
            subprocess.Popen(["python3", str(Path.home() / "lewis" / "lewis_gui.py")])
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Could not launch LEWIS: {e}")

if __name__ == "__main__":
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            prefs = f.read()
            if "skip_intro=True" in prefs:
                subprocess.Popen(["python3", str(Path.home() / "lewis" / "lewis_gui.py")])
                exit()

    root = tk.Tk()
    app = FirstTimeSetup(root)
    root.mainloop()
