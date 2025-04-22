import traceback
from core.self_modification import SelfEditor  # Import the SelfEditor class responsible for modifying code

class SelfHealing:
    def __init__(self):
        """
        Initializes the SelfHealing class and maps common errors to their possible fixes.
        """
        # Create an instance of SelfEditor that will handle code fixes
        self.editor = SelfEditor()  
        
        # Error map: Defines known error patterns and their corresponding fix actions.
        # The key is the error message, and the value is a tuple with the fix and the disabled fix.
        self.error_map = {
            "NameError: name 'foo' is not defined": ("foo()", "bar()"),  # Fix for undefined variable (foo -> bar)
            "ModuleNotFoundError: No module named 'some_module'": (
                "import some_module",  # Add missing import statement
                "# import some_module  # Disabled by self-healing"  # Comment out the import to prevent failure
            )
        }

    def monitor_and_heal(self, file_path, func):
        """
        Monitors a function for errors and attempts to auto-heal based on predefined error patterns.
        
        Arguments:
        file_path -- The path to the file where the error occurred.
        func -- The function to monitor for errors.
        """
        try:
            func()  # Attempt to run the function passed in the argument
        except Exception as e:
            # If an error occurs, capture the exception message
            error_msg = str(e)
            print(f"[!] Error Detected in {file_path}: {error_msg}")  # Output the error message

            # Check if the error message matches any known patterns in the error map
            for err in self.error_map:
                if err in error_msg:
                    print("[*] Attempting auto-heal...")  # Notify that an auto-heal attempt is being made
                    # Call the SelfEditor instance to fix the error in the code file
                    self.editor.auto_fix(file_path, self.error_map)
                    break  # Once a fix is applied, exit the loop

            # Log the full stack trace of the error to the editor's log file for debugging
            self.editor.log_error(file_path, traceback.format_exc())

# ✅ Wrapper function to be used in CLI
def auto_fix(error_msg):
    """
    Basic fix strategy based on error messages. Provides possible solutions for common errors.
    
    Arguments:
    error_msg -- The error message string to analyze.
    
    Returns:
    A string with the recommended fix or further investigation instructions.
    """
    # Handle specific types of errors and provide a fix strategy for each
    if "not defined" in error_msg:
        return "Possible fix: Did you forget to define a variable or function?"
    elif "No module named" in error_msg:
        return "Try installing the missing module with pip. For example: pip install some_module"
    elif "Permission denied" in error_msg:
        return "Try using sudo or check file permissions to ensure the correct access rights."
    else:
        return "Sorry, no auto-fix found for this error. Please investigate further."
