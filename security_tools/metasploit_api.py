# lewis/security_tools/metasploit_api.py

import subprocess

def run_msfconsole(module, options):
    try:
        command = f"use {module}\n"
        for key, value in options.items():
            command += f"set {key} {value}\n"
        command += "run\nexit\n"

        with open("msf_temp.rc", "w") as f:
            f.write(command)

        print("[+] Launching Metasploit with custom script...")
        output = subprocess.check_output(["msfconsole", "-r", "msf_temp.rc"], stderr=subprocess.STDOUT, text=True)
        return output

    except subprocess.CalledProcessError as e:
        return f"Error with Metasploit: {e.output}"
