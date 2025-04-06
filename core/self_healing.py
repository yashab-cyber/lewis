# core/self_healing.py

import traceback
from core.self_modification import SelfEditor

class SelfHealing:
    def __init__(self):
        self.editor = SelfEditor()
        self.error_map = {
            "NameError: name 'foo' is not defined": ("foo()", "bar()"),
            "ModuleNotFoundError: No module named 'some_module'": (
                "import some_module",
                "# import some_module  # Disabled by self-healing"
            )
        }

    def monitor_and_heal(self, file_path, func):
        try:
            func()
        except Exception as e:
            error_msg = str(e)
            print(f"[!] Error Detected in {file_path}: {error_msg}")
            for err in self.error_map:
                if err in error_msg:
                    print("[*] Attempting auto-heal...")
                    self.editor.auto_fix(file_path, self.error_map)
                    break
            self.editor.log_error(file_path, traceback.format_exc())
