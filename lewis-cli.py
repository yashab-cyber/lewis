#!/usr/bin/env python3

import argparse
from core.command_handler import handle_command
from core.ai_engine import generate_response
from core.self_healing import auto_fix
from security_tools import nmap_wrapper, nikto_integration
from ml_models.threat_detection import predict_threat

def main():
    parser = argparse.ArgumentParser(description="LEWIS CLI - Linux Environment Working Intelligence System")
    parser.add_argument("-q", "--query", help="Ask a question or give a command to LEWIS")
    args = parser.parse_args()

    if args.query:
        print(f"\n[+] You asked: {args.query}")

        # AI understanding and intent classification
        response, intent = generate_response(args.query)
        print(f"[AI] {response}\n")

        if intent == "run_nmap":
            target = input("Enter target IP/domain: ")
            print(nmap_wrapper.run_nmap(target))

        elif intent == "run_nikto":
            target = input("Enter target IP/domain: ")
            print(nikto_integration.run_nikto(target))

        elif intent == "predict_threat":
            logs = input("Paste system logs or output: ")
            print("[ML] Predicted Threat Level:", predict_threat(logs))

        elif intent == "self_heal":
            error_msg = input("Paste the error message: ")
            print(auto_fix(error_msg))

        else:
            print("[LEWIS] Command understood but no module attached yet.")

    else:
        print("[-] Please use -q to ask something. Example:\n")
        print("    python lewis-cli.py -q 'Scan this IP with Nmap'\n")

if __name__ == "__main__":
    main()
