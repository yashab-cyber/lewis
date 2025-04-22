# lewis/core/voice_interface.py

import pyttsx3
import speech_recognition as sr

class VoiceInterface:
    def __init__(self, trigger_word="hey lewis"):
        """
        Initializes voice engine and recognizer with trigger word.
        """
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.trigger_word = trigger_word.lower()

    def speak(self, text):
        """
        Convert text to speech output.
        """
        print(f"[LEWIS 🔊]: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        """
        Listen for voice input and convert it to text.
        Returns transcribed text or error message.
        """
        with sr.Microphone() as source:
            print("[LEWIS 🎤]: Listening for command...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

            try:
                text = self.recognizer.recognize_google(audio)
                return text.lower()
            except sr.UnknownValueError:
                return ""
            except sr.RequestError:
                return "speech recognition service is down"

    def activate(self):
        """
        Waits for the trigger word and enters command mode when heard.
        """
        self.speak("LEWIS is now active. Say 'Hey LEWIS' to start.")

        while True:
            command = self.listen()
            if self.trigger_word in command:
                self.speak("Yes? I'm listening.")
                self.command_mode()

            elif command in ["exit", "quit", "stop", "shutdown"]:
                self.speak("Shutting down voice interface. Bye.")
                break

    def command_mode(self):
        """
        Activated when trigger word is detected. Awaits one command.
        """
        self.speak("Please give your command.")
        command = self.listen()

        if not command:
            self.speak("Sorry, I didn’t catch that.")
        else:
            self.speak(f"You said: {command}")
            # You can route the command to LEWIS's main logic here
            # e.g., self.process_command(command)

# Example usage:
if __name__ == "__main__":
    vi = VoiceInterface()
    vi.activate()
