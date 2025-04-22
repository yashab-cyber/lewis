#!/usr/bin/env python3

import argparse
import logging
from core.command_handler import CommandHandler
from core.ai_engine import generate_response
from core.self_healing import auto_fix
from security_tools import nmap_wrapper, nikto_integration
from ml_models.threat_detection import detect_threat
from core.ai_engine import generate_response, hybrid_threat_analysis



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
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="LEWIS CLI - Linux Environment Working Intelligence System")
    parser.add_argument("-q", "--query", help="Ask a question or give a command to LEWIS")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("-t", "--target", help="Target IP/domain for scan commands")
    parser.add_argument("-l", "--loglevel", choices=["DEBUG", "INFO", "ERROR"], default="INFO", help="Set log level")
    args = parser.parse_args()

    # Setup logging based on the log level argument
    setup_logging(args.loglevel)
    
    if args.query:
        logging.info(f"User query: {args.query}")
        print(f"\n[+] You asked: {args.query}")

        try:
            # AI understanding and intent classification
            response, intent = generate_response(args.query)
            print(f"[AI] {response}\n")
            
            # Handling different intents
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
                logs = input("Paste system logs or CSV content (text or metrics):\n")
                print("[LEWIS] Running hybrid threat analysis...")

                try:
                    results = hybrid_threat_analysis(logs)
                    for model_type, result in results.items():
                        print(f"[{model_type}] {result}")
                    logging.info("Hybrid threat analysis completed.")
                except Exception as e:
                     print(f"[ERROR] Hybrid analysis failed: {e}")
                     logging.error(f"Hybrid analysis failed: {e}")
                             
            elif intent == "self_heal":
                if args.target:
                    error_msg = input("Paste the error message for self-healing: ")
                    if error_msg:
                        print(auto_fix(error_msg))
                        logging.info(f"Self-healing triggered for error: {error_msg}")
                    else:
                        print("[ERROR] Invalid error message for self-healing.")
                        logging.error("Invalid error message for self-healing.")
                else:
                    print("[ERROR] No target or log file provided for self-healing.")
                    logging.error("No target or log file provided for self-healing.")

            elif intent == "general_query":
                # General knowledge fallback handled here
                print(f"[LEWIS] {response}")
                logging.info(f"General query handled: {response}")

            else:
                # Catch-all for unhandled intents
                print(f"[LEWIS] {response}")
                logging.info(f"Unhandled intent: {response}")

        except Exception as e:
            print(f"[ERROR] An error occurred: {e}")
            logging.error(f"Error processing query '{args.query}': {e}")

    else:
        print("[-] Please use -q to ask something. Example:\n")
        print("    python lewis-cli.py -q 'Scan this IP with Nmap'\n")

if __name__ == "__main__":
    main()
