#!/usr/bin/env python3

import argparse
import logging
from core.command_handler import CommandHandler
from core.ai_engine import generate_response, hybrid_threat_analysis
from core.self_healing import SelfHealing
from security_tools import nmap_wrapper, nikto_integration
from ml_models.threat_detection import detect_threat

# Set up logging with advanced levels
def setup_logging(log_level):
    log_levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "ERROR": logging.ERROR
    }
    logging.basicConfig(filename='lewis_cli.log', level=log_levels.get(log_level, logging.INFO), 
                        format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    parser = argparse.ArgumentParser(description="LEWIS CLI - Linux Environment Working Intelligence System")
    parser.add_argument("-q", "--query", help="Ask a question or give a command to LEWIS")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("-t", "--target", help="Target IP/domain or file path")
    parser.add_argument("-l", "--loglevel", choices=["DEBUG", "INFO", "ERROR"], default="INFO", help="Set log level")
    args = parser.parse_args()

    setup_logging(args.loglevel)
    
    if args.query:
        logging.info(f"User query: {args.query}")
        print(f"\n[+] You asked: {args.query}")

        try:
            response, intent = generate_response(args.query)
            print(f"[AI] {response}\n")

            if intent == "run_nmap":
                if args.target:
                    print(nmap_wrapper.run_nmap(args.target))
                    logging.info(f"Nmap scan executed on {args.target}")
                else:
                    print("[ERROR] No target provided for Nmap scan.")
                    logging.error("No target provided for Nmap scan.")

            elif intent == "run_nikto":
                if args.target:
                    print(nikto_integration.run_nikto(args.target))
                    logging.info(f"Nikto scan executed on {args.target}")
                else:
                    print("[ERROR] No target provided for Nikto scan.")
                    logging.error("No target provided for Nikto scan.")

            elif intent == "predict_threat":
                logs = input("Paste system logs or CSV content:\n")
                print("[LEWIS] Running hybrid threat analysis...")
                try:
                    results = hybrid_threat_analysis(logs)
                    for model_type, result in results.items():
                        print(f"[{model_type}] {result}")
                    logging.info("Hybrid threat analysis completed.")
                except Exception as e:
                    print(f"[ERROR] Hybrid analysis failed: {e}")
                    logging.error(f"Hybrid analysis failed: {e}")

            elif intent == "monitor_script":
                if args.target:
                    healer = SelfHealing()
                    healer.run_healing_async(args.target)
                    print(f"[LEWIS] Monitoring and healing started on: {args.target}")
                    logging.info(f"Started healing thread on: {args.target}")
                else:
                    print("[ERROR] No target Python script provided.")
                    logging.error("No script provided for monitoring.")

            elif intent == "self_heal":
                if args.target:
                    error_msg = input("Paste the error message for self-healing: ")
                    if error_msg:
                        print("[LEWIS] Manual healing is deprecated. Use monitor_script instead.")
                        logging.warning("Manual healing flow triggered.")
                    else:
                        print("[ERROR] Invalid error message.")
                        logging.error("Invalid self-healing input.")
                else:
                    print("[ERROR] No file provided for self-healing.")
                    logging.error("No file path for healing.")

            elif intent == "general_query":
                print(f"[LEWIS] {response}")
                logging.info(f"General query handled.")

            else:
                print(f"[LEWIS] {response}")
                logging.info(f"Unhandled intent.")

        except Exception as e:
            print(f"[ERROR] Exception: {e}")
            logging.error(f"Exception during query '{args.query}': {e}")

    else:
        print("[-] Please use -q to ask something. Example:\n")
        print("    python lewis-cli.py -q 'Heal this script' -t path/to/script.py\n")

if __name__ == "__main__":
    main()
