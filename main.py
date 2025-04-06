# lewis/main.py

from core.ai_engine import LewisAI
from core.command_handler import CommandHandler
from core.self_healing import SelfHealing
from core.voice_interface import VoiceInterface

def main():
    ai = LewisAI()
    cmd_handler = CommandHandler()
    healer = SelfHealing()
    voice = VoiceInterface()

    print(ai.introduce())
    ai.speak = voice.speak  # Connect voice to AI if needed

    while True:
        print("\nChoose an option:")
        print("1. Text Chat with LEWIS")
        print("2. Run a Command")
        print("3. Use Voice")
        print("4. Show Threat Learning")
        print("5. Exit")
        
        choice = input("Enter option number: ")

        if choice == "1":
            user_input = input("You: ")
            response = ai.chat(user_input)
            print(f"LEWIS: {response}")
            ai.speak(response)

        elif choice == "2":
            command = input("Enter terminal command: ")
            output = cmd_handler.execute(command)
            print(output)
            if "Error" in output or "not allowed" in output:
                healer.log_error(output)
                print("LEWIS self-healing: ", healer.attempt_fix(output))

        elif choice == "3":
            voice.speak("Say something...")
            spoken = voice.listen()
            print("You said:", spoken)
            response = ai.chat(spoken)
            print(f"LEWIS: {response}")
            voice.speak(response)

        elif choice == "4":
            print(ai.get_threat_insights())

        elif choice == "5":
            print("Exiting LEWIS. Stay secure!")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
