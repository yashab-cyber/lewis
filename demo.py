#!/usr/bin/env python3
"""
LEWIS Demo Script
Demonstrates core functionality of the LEWIS system
"""

import asyncio
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config.settings import Settings
from utils.logger import setup_logger
from core.lewis_core import LewisCore

async def run_demo():
    """Run LEWIS demonstration"""
    print("""
    ██╗     ███████╗██╗    ██╗██╗███████╗
    ██║     ██╔════╝██║    ██║██║██╔════╝
    ██║     █████╗  ██║ █╗ ██║██║███████╗
    ██║     ██╔══╝  ██║███╗██║██║╚════██║
    ███████╗███████╗╚███╔███╔╝██║███████║
    ╚══════╝╚══════╝ ╚══╝╚══╝ ╚═╝╚══════╝
    
    LEWIS Demo - Testing Core Functionality
    """)
    
    try:
        # Initialize LEWIS
        print("🔧 Initializing LEWIS...")
        settings = Settings()
        logger = setup_logger()
        lewis = LewisCore(settings, logger)
        
        print("✅ LEWIS initialized successfully\n")
        
        # Test commands
        test_commands = [
            "what is nmap?",
            "help me scan a network",
            "tell me about web vulnerabilities", 
            "how do I use nikto?",
            "generate a security report"
        ]
        
        print("🧪 Running test commands...\n")
        
        for i, command in enumerate(test_commands, 1):
            print(f"📝 Test {i}: {command}")
            print("-" * 50)
            
            try:
                result = await lewis.process_command(command, "demo_user")
                
                if result.get("success"):
                    ai_response = result.get("ai_response", {})
                    response_text = ai_response.get("text", "No response")
                    intent = ai_response.get("intent", "unknown")
                    
                    print(f"🎯 Intent: {intent}")
                    print(f"🤖 Response: {response_text[:200]}...")
                    
                    if ai_response.get("suggestions"):
                        print(f"💡 Suggestions: {', '.join(ai_response['suggestions'][:3])}")
                    
                    print("✅ Command processed successfully")
                else:
                    print(f"❌ Error: {result.get('error')}")
                    
            except Exception as e:
                print(f"❌ Test failed: {e}")
            
            print("\n")
        
        # System status
        print("📊 System Status:")
        print("-" * 30)
        status = lewis.get_system_status()
        
        for component, ready in status.get("components", {}).items():
            status_icon = "✅" if ready else "❌"
            print(f"{status_icon} {component.replace('_', ' ').title()}")
        
        print(f"\n🔧 Available Tools: {status.get('stats', {}).get('tools', 0)}")
        print(f"📚 Knowledge Entries: {status.get('stats', {}).get('knowledge_entries', 0)}")
        
        # Cleanup
        lewis.shutdown()
        
        print("\n🎉 Demo completed successfully!")
        print("Ready to use LEWIS for cybersecurity tasks!")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return False
    
    return True

def main():
    """Main demo function"""
    try:
        # Run async demo
        success = asyncio.run(run_demo())
        
        if success:
            print("\n✅ LEWIS is ready for use!")
            print("Start with: python lewis.py --mode cli")
        else:
            print("\n❌ Demo encountered issues")
            print("Check the logs for more information")
            
    except KeyboardInterrupt:
        print("\n🛑 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
