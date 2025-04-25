import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog
import subprocess
import threading
import time
import os

from lewis_cyber_law_audit.lewis_gui_law_audit import CyberLawAuditFrame
from core.lewis_runner import LewisCore

from core.self_healing import CodeMonitorHandler
from core.self_learning import SelfLearner
from core.self_modification import SelfModifier
from watchdog.observers import Observer


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
        self.tab_audit = self.create_tab(notebook, "lewis cli")
        self.tab_vapt = self.create_tab(notebook, "VAPT")
        self.tab_ai = self.create_tab(notebook, "AI")
        self.tab_logs = self.create_tab(notebook, "Logs")
        self.tab_law = self.create_tab(notebook, "Cyber Law Audit")

        self.create_cli_tab()
        self.create_log_tab()
        self.lewis = LewisCore()
        self.create_ai_tab()
        self.create_vapt_tab()

        # Cyber Law Audit Frame
        CyberLawAuditFrame(self.tab_law).pack(fill="both", expand=True)

        # Start AI self features
        self.start_self_learning()
        self.start_self_modification()
        self.start_self_healing()

    def create_tab(self, notebook, title):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=title)
        return frame

    def create_ai_tab(self):
        self.ai_output = scrolledtext.ScrolledText(self.tab_ai, bg="#1e1e1e", fg="#00ffcc", insertbackground="white")
        self.ai_output.pack(fill="both", expand=True, padx=10, pady=(10, 5))

        ttk.Button(self.tab_ai, text="Chat with LEWIS (Text)", command=self.ask_lewis).pack(pady=5)
        ttk.Button(self.tab_ai, text="Voice Chat (Once)", command=self.voice_lewis).pack(pady=5)
        ttk.Button(self.tab_ai, text="Run Terminal Command", command=self.run_terminal_command).pack(pady=5)
        ttk.Button(self.tab_ai, text="Show Threat Learning", command=self.show_threats).pack(pady=5)

    def create_cli_tab(self):
      self.output_text = scrolledtext.ScrolledText(self.tab_audit, bg="#1e1e1e", fg="#00ffcc", insertbackground="white")
      self.output_text.pack(fill="both", expand=True, padx=10, pady=(10, 5))

      input_frame = ttk.Frame(self.tab_audit)
      input_frame.pack(fill="x", padx=10, pady=(0, 10))

      self.command_entry = ttk.Entry(input_frame)
      self.command_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
      self.command_entry.bind("<Return>", lambda event: self.send_input())

      send_btn = ttk.Button(input_frame, text="Send to LEWIS CLI", command=self.send_input)
      send_btn.pack(side="right")

      ttk.Button(self.tab_audit, text="Run LEWIS Core", command=self.run_main).pack(pady=(0, 10))


    def create_vapt_tab(self):
        ttk.Button(self.tab_vapt, text="Start Full VAPT Scan", command=self.run_vapt_gui).pack(pady=20)

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

    def ask_lewis(self):
        user_input = simpledialog.askstring("Chat with LEWIS", "Type your question:")
        if user_input:
            response = self.lewis.text_chat(user_input)
            self.ai_output.insert(tk.END, f"You: {user_input}\nLEWIS: {response}\n")
            self.ai_output.see(tk.END)

    def voice_lewis(self):
        spoken, response = self.lewis.voice_once()
        self.ai_output.insert(tk.END, f"You said: {spoken}\nLEWIS: {response}\n")
        self.ai_output.see(tk.END)

    def run_terminal_command(self):
        command = simpledialog.askstring("Run Terminal Command", "Enter command:")
        if command:
            output = self.lewis.run_command(command)
            self.ai_output.insert(tk.END, f"Command: {command}\nOutput:\n{output}\n")
            self.ai_output.see(tk.END)

    def show_threats(self):
        insights = self.lewis.show_threat_learning()
        self.ai_output.insert(tk.END, f"Threat Insights:\n{insights}\n")
        self.ai_output.see(tk.END)

    def send_input(self):
     command = self.command_entry.get().strip()
     if not command:
        return

     self.output_text.insert(tk.END, f"> {command}\n")
     self.output_text.see(tk.END)
     self.command_entry.delete(0, tk.END)

     try:
        # Call lewis-cli.py with -q argument
        result = subprocess.run(
            ['python', 'lewis-cli.py', '-q', command],
            capture_output=True,
            text=True
        )
        self.output_text.insert(tk.END, result.stdout + '\n')
        if result.stderr:
            self.output_text.insert(tk.END, f"[Error]\n{result.stderr}\n")

     except Exception as e:
        self.output_text.insert(tk.END, f"[Exception] {str(e)}\n")

     self.output_text.see(tk.END)


    def run_main(self):
        self.output_text.insert(tk.END, "LEWIS core is running. Ready to accept commands.\n")
        self.output_text.see(tk.END)

    # ✅ Self Features Start Automatically

    def start_self_learning(self):
        def run_learning():
            log_path = "lewis_error.log"
            if not os.path.exists(log_path):
                open(log_path, "w").close()

            learner = SelfLearner(log_path)
            while True:
                learner.learn_from_logs()
                time.sleep(10)

        threading.Thread(target=run_learning, daemon=True).start()

    def start_self_modification(self):
        def run_modification():
            log_path = "lewis_error.log"
            if not os.path.exists(log_path):
                open(log_path, "w").close()

            modifier = SelfModifier(log_path)
            while True:
                modifier.modify_code_based_on_learning()
                time.sleep(15)

        threading.Thread(target=run_modification, daemon=True).start()

    def start_self_healing(self):
        def run_healing():
            event_handler = CodeMonitorHandler()
            observer = Observer()
            observer.schedule(event_handler, path='.', recursive=True)
            observer.start()
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                observer.stop()
            observer.join()

        threading.Thread(target=run_healing, daemon=True).start()
    
    def run_vapt_gui(self):
     try:
        from core.vapt_engine import VAPTEngine
     except ImportError:
        messagebox.showerror("Import Error", "VAPT module not found.")
        return

     target = simpledialog.askstring("VAPT Scan", "Enter target IP or domain:")
     if not target:
        return

     vapt = VAPTEngine()
     result = vapt.full_scan(target)

     messagebox.showinfo("VAPT Completed", result)


if __name__ == "__main__":
    app = LewisGUI()
    app.mainloop()
