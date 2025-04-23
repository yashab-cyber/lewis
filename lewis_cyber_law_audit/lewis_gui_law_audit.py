import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter import scrolledtext
import importlib.util
import os
import csv
import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import datetime
import threading

class CyberLawAuditFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.selected_file = ""
        self.options = {
            "India (IT Act)": "india",
            "GDPR": "gdpr",
            "ISO 27001": "iso_27001",
            "HIPAA": "hipaa",
            "PCI DSS": "pci_dss"
        }
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Cyber Law Compliance Audit", font=("Segoe UI", 14, "bold")).pack(pady=10)

        tk.Button(self, text="📂 Browse PDF", command=self.browse_file).pack(pady=5)
        self.file_label = tk.Label(self, text="", wraplength=700)
        self.file_label.pack(pady=3)

        self.progress = tk.Label(self, text="Waiting to run audit...", fg="blue")
        self.progress.pack(pady=3)

        tk.Button(self, text="⚙️ Run Full Audit (All Laws)", command=self.run_full_audit_threaded).pack(pady=10)

        self.result_text = scrolledtext.ScrolledText(self, wrap="word", bg="#0e0e0e", fg="#00ff88",
                                                     font=("Consolas", 10), height=25)
        self.result_text.pack(fill="both", expand=True, padx=10, pady=10)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="📄 Save PDF", command=self.save_as_pdf).pack(side="left", padx=5)
        tk.Button(btn_frame, text="🧾 Save CSV", command=self.save_as_csv).pack(side="left", padx=5)

    def browse_file(self):
        self.selected_file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        self.file_label.config(text=self.selected_file)

    def load_rules(self, module_name):
        try:
            module_path = f"modules/law_audit/rules/{module_name}.py"
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return getattr(mod, f"get_{module_name}_rules")()
        except Exception as e:
            return []

    def run_full_audit_threaded(self):
        threading.Thread(target=self.run_full_audit).start()

    def run_full_audit(self):
        if not self.selected_file or not os.path.isfile(self.selected_file):
            messagebox.showerror("Error", "Please select a valid PDF file.")
            return

        self.result_text.delete("1.0", tk.END)
        self.progress.config(text="🔍 Running full audit...", fg="orange")
        self.audit_results = {}

        try:
            with open(self.selected_file, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                content = "".join([page.extract_text() or "" for page in reader.pages])

            for law, module_key in self.options.items():
                self.result_text.insert(tk.END, f"\n=== {law} ===\n")
                rules = self.load_rules(module_key)
                passed = 0
                law_results = []

                for rule in rules:
                    if rule.lower() in content.lower():
                        self.result_text.insert(tk.END, f"✅ {rule}\n")
                        law_results.append((rule, True))
                        passed += 1
                    else:
                        self.result_text.insert(tk.END, f"❌ {rule}\n")
                        law_results.append((rule, False))

                score = int((passed / len(rules)) * 100) if rules else 0
                self.result_text.insert(tk.END, f"➡️ Compliance Score: {score}%\n")
                self.audit_results[law] = {
                    "rules": law_results,
                    "score": score
                }

            self.progress.config(text="✅ Full audit completed", fg="green")

        except Exception as e:
            self.progress.config(text="❌ Audit failed", fg="red")
            messagebox.showerror("Audit Error", str(e))

    def save_as_pdf(self):
        if not hasattr(self, "audit_results") or not self.audit_results:
            messagebox.showerror("Error", "Run the audit first.")
            return

        filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not filename:
            return

        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4
        y = height - 50

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, y, "LEWIS Cyber Law Audit Report")
        y -= 30
        c.setFont("Helvetica", 12)
        c.drawString(50, y, f"File: {os.path.basename(self.selected_file)}")
        y -= 20
        c.drawString(50, y, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        y -= 40

        for law, data in self.audit_results.items():
            c.setFont("Helvetica-Bold", 13)
            c.drawString(50, y, f"=== {law} ===")
            y -= 20
            c.setFont("Helvetica", 10)
            for rule, passed in data["rules"]:
                status = "✅" if passed else "❌"
                c.drawString(60, y, f"{status} {rule}")
                y -= 15
                if y < 50:
                    c.showPage()
                    y = height - 50
            c.drawString(60, y, f"Compliance Score: {data['score']}%")
            y -= 30

        c.save()
        messagebox.showinfo("Saved", "PDF Report saved successfully!")

    def save_as_csv(self):
        if not hasattr(self, "audit_results") or not self.audit_results:
            messagebox.showerror("Error", "Run the audit first.")
            return

        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not filename:
            return

        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Law", "Rule", "Passed", "Score (%)"])
            for law, data in self.audit_results.items():
                for rule, passed in data["rules"]:
                    writer.writerow([law, rule, "Yes" if passed else "No", data["score"]])

        messagebox.showinfo("Saved", "CSV Report saved successfully!")
