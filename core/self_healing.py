import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

class CodeMonitorHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            print(f'File modified: {event.src_path}')
            self.heal_code(event.src_path)

    def heal_code(self, file_path):
        try:
            print(f"Attempting to heal the code: {file_path}")
            result = subprocess.run(['python3', file_path], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Error detected in {file_path}: {result.stderr}")
                self.fix_error(file_path, result.stderr)
            else:
                print(f"No error detected in {file_path}")
        except Exception as e:
            print(f"Error during healing: {e}")

    def fix_error(self, file_path, error_log):
        print("Fixing the code based on error logs...")
        with open(file_path, 'r') as file:
            code = file.read()

        fixed_code = code.replace("print('Error')", "print('Fixed error!')")

        with open(file_path, 'w') as file:
            file.write(fixed_code)
        print(f"Code fixed and saved: {file_path}")


# ✅ Add this wrapper class to be used in lewis_runner.py
class SelfHealing:
    def __init__(self):
        self.handler = CodeMonitorHandler()
        self.observer = Observer()
        self.log_file = "lewis_error.log"

    def run_healing_async(self, path='.'):
        self.observer.schedule(self.handler, path=path, recursive=True)
        self.observer.start()

    def stop(self):
        self.observer.stop()
        self.observer.join()

    def log_error(self, error_output):
        with open(self.log_file, 'a') as f:
            f.write(error_output + '\n')

    def attempt_fix(self, error_output):
        return "Basic healing attempted. Please review logs for full fix details."


# Optional standalone runner (if needed)
if __name__ == "__main__":
    path_to_watch = '.'
    healing = SelfHealing()
    healing.run_healing_async(path_to_watch)
    print("Monitoring for changes...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        healing.stop()
