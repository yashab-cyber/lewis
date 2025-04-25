import os
from datetime import datetime
from security_tools import nmap_wrapper, nikto_integration, metasploit_api

class VAPTEngine:
    def __init__(self):
        self.report_dir = "vapt_reports"
        os.makedirs(self.report_dir, exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.report_path = os.path.join(self.report_dir, f"report_{self.timestamp}.txt")

    def log(self, label, data):
        with open(self.report_path, "a") as f:
            f.write(f"\n=== {label} ===\n{data}\n")

    def scan_nmap(self, target):
        result = nmap_wrapper.run_nmap(target)
        self.log("Nmap Scan", result)
        return result

    def scan_nikto(self, target):
        result = nikto_integration.run_nikto(target)
        self.log("Nikto Scan", result)
        return result

    def exploit_metasploit(self, module, options):
        result = metasploit_api.run_msfconsole(module, options)
        self.log("Metasploit Exploit", result)
        return result

    def full_scan(self, target):
        print(f"[+] Starting full scan on {target}")
        output = self.scan_nmap(target)
        print("[Nmap] Done.")

        if target.startswith("http://") or target.startswith("https://"):
            output += "\n" + self.scan_nikto(target)
            print("[Nikto] Done.")
        else:
            print("[Nikto] Skipped (not HTTP).")

        return f"Scan report saved: {self.report_path}"
