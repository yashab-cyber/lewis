# lewis/security_tools/nikto_integration.py

import subprocess

def run_nikto(target):
    try:
        print(f"[+] Scanning {target} with Nikto")
        result = subprocess.check_output(["nikto", "-h", target], stderr=subprocess.STDOUT, text=True)
        return result
    except subprocess.CalledProcessError as e:
        return f"Error running Nikto: {e.output}"
