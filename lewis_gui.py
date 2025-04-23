
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import threading
from lewis_cyber_law_audit.lewis_gui_law_audit import CyberLawAuditFrame

class LewisGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LEWIS – Cybersecurity AI Assistant")
        self.geometry("800x600")
        self.configure(bg="#0f0f0f")

        style = ttk.Style(self)
        style.theme_use('default')
        style.configure('TNotebook.Tab', background="#1e1e1e", foreground="#00ffcc")
        style.configure('TNotebook', background="#0f0f0f")
        style.map("TNotebook.Tab", background=[("selected", "#00ffcc")], foreground=[("selected", "#0f0f0f")])

        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True)

        # Tabs
        self.tab_audit = self.create_tab(notebook, "Audit")
        self.tab_vapt = self.create_tab(notebook, "VAPT")
        self.tab_ai = self.create_tab(notebook, "AI")
        self.tab_logs = self.create_tab(notebook, "Logs")
        self.tab_law = self.create_tab(notebook, "Cyber Law Audit")

        self.create_audit_tab()
        self.create_log_tab()

        # Load Cyber Law Audit Frame
        CyberLawAuditFrame(self.tab_law).pack(fill="both", expand=True)

    def create_tab(self, notebook, title):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=title)
        return frame

    def create_audit_tab(self):
        run_button = ttk.Button(self.tab_audit, text="Run LEWIS ", command=self.run_main)
        run_button.pack(pady=20)

        self.output_text = scrolledtext.ScrolledText(self.tab_audit, bg="#1e1e1e", fg="#00ffcc", insertbackground="white")
        self.output_text.pack(fill="both", expand=True, padx=10, pady=10)

    def create_log_tab(self):
        self.log_viewer = scrolledtext.ScrolledText(self.tab_logs, bg="#1e1e1e", fg="#00ffcc", insertbackground="white")
        self.log_viewer.pack(fill="both", expand=True, padx=10, pady=10)
        self.load_logs()

    def load_logs(self):
        try:
            with open("lewis_ai.log", "r") as log_file:
                self.log_viewer.insert("1.0", log_file.read())
        except FileNotFoundError:
            self.log_viewer.insert("1.0", "Log file not found.")

    def run_main(self):
        def execute():
            self.output_text.delete("1.0", tk.END)
            try:
                process = subprocess.Popen(["python3", "main.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                for line in process.stdout:
                    self.output_text.insert(tk.END, line)
                    self.output_text.see(tk.END)
                for err in process.stderr:
                    self.output_text.insert(tk.END, f"ERR: {err}", "err")
                    self.output_text.see(tk.END)
            except Exception as e:
                messagebox.showerror("Execution Error", str(e))

        threading.Thread(target=execute).start()

if __name__ == "__main__":
    app = LewisGUI()
    app.mainloop()
