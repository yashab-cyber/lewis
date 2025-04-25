import sys
from core.ai_engine import LewisAI
from core.command_handler import CommandHandler
from core.self_healing import SelfHealing
from core.voice_interface import VoiceInterface

def interactive_mode(ai, cmd_handler, healer, voice):
    print(ai.introduce(), flush=True)
    ai.speak = voice.speak

    while True:
        print("\nChoose an option:", flush=True)
        print("1. Text Chat with LEWIS", flush=True)
        print("2. Run a Command", flush=True)
        print("3. Use Voice Once", flush=True)
        print("4. Voice Trigger Mode", flush=True)
        print("5. Show Threat Learning", flush=True)
        print("6. Exit", flush=True)
        choice = input("Enter option number: ").strip()

        if choice == "1":
            user_input = input("You: ")
            response = ai.chat(user_input)
            print(f"LEWIS: {response}", flush=True)
            ai.speak(response)

        elif choice == "2":
            command = input("Enter terminal command: ")
            output = cmd_handler.execute(command)
            print(output, flush=True)
            if "Error" in output or "not allowed" in output:
                healer.log_error(output)
                print("LEWIS self-healing: ", healer.attempt_fix(output), flush=True)

        elif choice == "3":
            voice.speak("Say something...")
            spoken = voice.listen()
            print("You said:", spoken, flush=True)
            response = ai.chat(spoken)
            print(f"LEWIS: {response}", flush=True)
            voice.speak(response)

        elif choice == "4":
            voice.speak("Say a command when you're ready. Say 'exit' to stop.")
            while True:
                spoken = voice.listen()
                if "exit" in spoken.lower():
                    voice.speak("Exiting voice command mode.")
                    break
                print("You said:", spoken, flush=True)
                command = ai.interpret_command(spoken)
                if command:
                    output = cmd_handler.execute(command)
                    print(f"[Command]: {command}", flush=True)
                    print(f"[Output]:\n{output}", flush=True)
                    voice.speak("Command executed.")
                else:
                    response = ai.chat(spoken)
                    print(f"LEWIS: {response}", flush=True)
                    voice.speak(response)

        elif choice == "5":
            print(ai.get_threat_insights(), flush=True)

        elif choice == "6":
            print("Exiting LEWIS. Stay secure!", flush=True)
            break
        else:
            print("Invalid choice. Try again.", flush=True)

def main():
    ai = LewisAI()
    cmd_handler = CommandHandler()
    healer = SelfHealing()
    voice = VoiceInterface()

    if sys.stdin.isatty():
        # Running in terminal
        interactive_mode(ai, cmd_handler, healer, voice)
    else:
        # Running from GUI or piped input
        ai.speak = voice.speak
        print(ai.introduce(), flush=True)
        for line in sys.stdin:
            user_input = line.strip()
            if user_input.lower() in ["exit", "quit"]:
                print("Exiting LEWIS.", flush=True)
                break
            if user_input == "1":
                print("Text chat selected. Awaiting input...", flush=True)
            else:
                response = ai.chat(user_input)
                print(f"LEWIS: {response}", flush=True)

if __name__ == "__main__":
    main()
