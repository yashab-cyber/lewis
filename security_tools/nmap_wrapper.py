# lewis/security_tools/nmap_wrapper.py

import subprocess

def run_nmap(target):
    try:
        print(f"[+] Running Nmap on {target}")
        result = subprocess.check_output(["nmap", "-sV", target], stderr=subprocess.STDOUT, text=True)
        return result
    except subprocess.CalledProcessError as e:
        return f"Error running Nmap: {e.output}"
