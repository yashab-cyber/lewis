import subprocess
import difflib
import os
from datetime import datetime

COMMAND_LIST_PATH = "config/allowed_commands.list"
LOG_FILE = "logs/command_log.txt"

class CommandHandler:
    def __init__(self):
        self.allowed_commands = self.load_allowed_commands()

    def load_allowed_commands(self):
        allowed = []
        if not os.path.exists(COMMAND_LIST_PATH):
            return allowed

        with open(COMMAND_LIST_PATH, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    allowed.append(line)
        return allowed

    def is_allowed(self, cmd):
        return any(cmd.startswith(allowed) for allowed in self.allowed_commands)

    def suggest_command(self, cmd):
        suggestions = difflib.get_close_matches(cmd, self.allowed_commands, n=3, cutoff=0.5)
        return suggestions

    def categorize_commands(self):
        categories = {}
        current_category = "Uncategorized"

        with open(COMMAND_LIST_PATH, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("#"):
                    current_category = line.replace("#", "").strip()
                elif line:
                    categories.setdefault(current_category, []).append(line)
        return categories

    def log_command(self, cmd, output):
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, 'a') as f:
            f.write(f"[{datetime.now()}] Command: {cmd}\n")
            f.write(f"Output:\n{output}\n")
            f.write("="*60 + "\n")

    def execute(self, cmd):
        cmd = cmd.strip()

        if not self.is_allowed(cmd):
            suggestions = self.suggest_command(cmd)
            msg = f"\033[91m[!] Command not allowed: `{cmd}`\033[0m"
            if suggestions:
                msg += f"\n\033[93m[+] Did you mean:\n - " + "\n - ".join(suggestions) + "\033[0m"
            return msg

        # Confirm for sensitive commands
        if any(keyword in cmd for keyword in ["shadow", "passwd", "rm", "format", "mkfs", "shutdown", "reboot"]):
            confirm = input("\033[91m[!] This command may affect system integrity. Type 'yes' to proceed: \033[0m")
            if confirm.strip().lower() != "yes":
                return "[*] Command execution aborted."

        try:
            result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=30, universal_newlines=True)
            self.log_command(cmd, result)
            return f"\033[92m[OUTPUT]\033[0m\n{result}"
        except subprocess.CalledProcessError as e:
            return f"\033[91m[ERROR] Command failed:\033[0m\n{e.output}"
        except Exception as ex:
            return f"\033[91m[FATAL] {str(ex)}\033[0m"
