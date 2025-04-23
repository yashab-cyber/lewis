# core/self_modification.py

import difflib
import os
import datetime

class SelfEditor:
    def __init__(self, log_file='logs/self_modifications.log'):
        self.log_file = log_file
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

    def read_file(self, path):
        with open(path, 'r') as f:
            return f.readlines()

    def write_file(self, path, lines):
        with open(path, 'w') as f:
            f.writelines(lines)

    def patch_code(self, file_path, find_str, replace_str):
        try:
            lines = self.read_file(file_path)
            new_lines = [line.replace(find_str, replace_str) for line in lines]

            if lines != new_lines:
                self.write_file(file_path, new_lines)
                self.log_patch(file_path, find_str, replace_str, lines, new_lines)
                return True
            return False
        except Exception as e:
            self.log_error(file_path, str(e))
            return False

    def log_patch(self, file_path, find_str, replace_str, old_lines, new_lines):
        timestamp = datetime.datetime.now().isoformat()
        diff = ''.join(difflib.unified_diff(old_lines, new_lines, lineterm=''))
        with open(self.log_file, 'a') as log:
            log.write(f"[{timestamp}] PATCHED {file_path}\n")
            log.write(f"Find: {find_str}\nReplace: {replace_str}\n")
            log.write(f"Diff:\n{diff}\n\n")

    def log_error(self, file_path, error):
        timestamp = datetime.datetime.now().isoformat()
        with open(self.log_file, 'a') as log:
            log.write(f"[{timestamp}] ERROR in {file_path}: {error}\n\n")

    def auto_fix(self, file_path, error_map):
        """
        Automatically apply known fixes based on common error patterns.
        error_map = {
            'NameError: name\\'foo\\' is not defined': ('foo()', 'bar()')
        }
        """
        for error_pattern, (find_str, replace_str) in error_map.items():
            if self.patch_code(file_path, find_str, replace_str):
                print(f"Auto-fixed issue in {file_path} using pattern: {error_pattern}")
