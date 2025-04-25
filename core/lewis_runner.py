# core/lewis_runner.py

from core.ai_engine import LewisAI
from core.command_handler import CommandHandler
from core.self_healing import SelfHealing  # ✅ FIXED import
from core.voice_interface import VoiceInterface

class LewisCore:
    def __init__(self):
        self.ai = LewisAI()
        self.cmd_handler = CommandHandler()
        self.healer = SelfHealing()  # ✅ Now works
        self.voice = VoiceInterface()
        self.ai.speak = self.voice.speak  # Link voice output

    def text_chat(self, user_input):
        return self.ai.chat(user_input)

    def run_command(self, command):
        output = self.cmd_handler.execute(command)
        fix = ""
        if "Error" in output or "Exception" in output:
            self.healer.log_error(output)
            fix = self.healer.attempt_fix(output)
        return output + ("\n\nSelf-Healing: " + fix if fix else "")

    def voice_once(self):
        self.voice.speak("Say something...")
        spoken = self.voice.listen()
        response = self.ai.chat(spoken)
        self.voice.speak(response)
        return spoken, response

    def show_threat_learning(self):
        return self.ai.get_threat_insights()
