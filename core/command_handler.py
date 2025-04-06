# lewis/core/command_handler.py

import subprocess
import os
import yaml

class CommandHandler:
    def __init__(self, config_path='config/allowed_commands.list'):
        self.allowed = self.load_allowed_commands(config_path)

    def load_allowed_commands(self, path):
        if os.path.exists(path):
            with open(path, 'r') as file:
                return [line.strip() for line in file.readlines()]
        return []

    def is_safe_command(self, command):
        return any(cmd in command for cmd in self.allowed)

    def execute(self, command):
        if not self.is_safe_command(command):
            return "Command not allowed or is unsafe!"
        try:
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return result.stdout.decode() or result.stderr.decode()
        except Exception as e:
            return f"Error: {str(e)}"
