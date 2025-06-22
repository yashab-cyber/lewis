#!/usr/bin/env python3
"""
LEWIS - Linux Environment Working Intelligence System
Main Application Entry Point

This is the core application launcher that initializes all LEWIS components
and provides the main interface for the cybersecurity AI assistant.
"""

import os
import sys
import argparse
import logging
import asyncio
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.lewis_core import LewisCore
from config.settings import load_settings
from utils.logger import setup_logger

# Import interface modules
from interfaces.cli_interface import CLIInterface
from interfaces.gui_interface import GUIInterface
from interfaces.web_interface import create_web_interface

# Import additional modules
from voice.voice_assistant import create_voice_assistant
from analytics.analytics_engine import create_analytics_engine
from detection.threat_detection import create_threat_detection_engine

async def main():
    """Main entry point for LEWIS application"""
    parser = argparse.ArgumentParser(
        description="LEWIS - Linux Environment Working Intelligence System"
    )
    
    parser.add_argument(
        "--mode", 
        choices=["cli", "gui", "server"], 
        default="cli",
        help="Launch mode: CLI, GUI, or Server"
    )
    
    parser.add_argument(
        "--config", 
        default="config/config.yaml",
        help="Configuration file path"
    )
    
    parser.add_argument(
        "--debug", 
        action="store_true",
        help="Enable debug mode"
    )
    
    parser.add_argument(
        "--voice", 
        action="store_true",
        help="Enable voice assistant"
    )
    
    parser.add_argument(
        "--port", 
        type=int,
        default=8000,
        help="Port for server mode (default: 8000)"
    )
    
    parser.add_argument(
        "--host", 
        default="0.0.0.0",
        help="Host for server mode (default: 0.0.0.0)"
    )
    
    args = parser.parse_args()
    
    try:
        # Load configuration
        settings = load_settings(args.config)
        
        # Override debug setting
        if args.debug:
            settings.update({"logging": {"level": "DEBUG"}})
        
        # Override voice setting
        if args.voice:
            settings.update({"voice": {"enabled": True}})
        
        # Setup logging
        logger = setup_logger(settings)
        logger.info("Starting LEWIS - Linux Environment Working Intelligence System")
        logger.info(f"Launch mode: {args.mode}")
        
        # Initialize LEWIS core
        lewis_core = LewisCore(settings, logger)
        await lewis_core.initialize()
        
        # Load extensions
        logger.info("🔌 Loading extensions...")
        extension_count = lewis_core.load_extensions()
        if extension_count > 0:
            logger.info(f"✅ Loaded {extension_count} extensions")
        else:
            logger.info("ℹ️ No extensions loaded")
        
        # Initialize additional components
        components = {}
        
        # Voice assistant
        if settings.get("voice", {}).get("enabled", False):
            voice_assistant = create_voice_assistant(settings, logger)
            components["voice"] = voice_assistant
            logger.info("Voice assistant initialized")
        
        # Analytics engine
        analytics_engine = create_analytics_engine(settings, logger)
        components["analytics"] = analytics_engine
        logger.info("Analytics engine initialized")
        
        # Threat detection
        if settings.get("detection", {}).get("enabled", True):
            threat_detection = create_threat_detection_engine(settings, logger)
            components["threat_detection"] = threat_detection
            logger.info("Threat detection engine initialized")
        
        # Launch appropriate interface
        if args.mode == "cli":
            await launch_cli_mode(lewis_core, settings, logger, components)
        
        elif args.mode == "gui":
            await launch_gui_mode(lewis_core, settings, logger, components)
        
        elif args.mode == "server":
            await launch_server_mode(lewis_core, settings, logger, components, args.host, args.port)
        
    except KeyboardInterrupt:
        logger.info("Shutting down LEWIS...")
        await shutdown_components(components)
    
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        if args.debug:
            logger.exception("Full traceback:")
        sys.exit(1)

async def launch_cli_mode(lewis_core, settings, logger, components):
    """Launch CLI interface"""
    logger.info("Launching CLI interface")
    
    cli_interface = CLIInterface(lewis_core, settings, logger)
    
    # Set up voice assistant if available
    if "voice" in components:
        voice_assistant = components["voice"]
        voice_assistant.set_command_processor(lewis_core.process_command)
        
        # Start voice assistant in background
        voice_task = asyncio.create_task(voice_assistant.start_voice_assistant())
    
    # Start background tasks
    background_tasks = []
    
    if "analytics" in components:
        background_tasks.append(
            asyncio.create_task(components["analytics"].start_analytics_engine())
        )
    
    if "threat_detection" in components:
        background_tasks.append(
            asyncio.create_task(components["threat_detection"].start_threat_detection())
        )
    
    # Start CLI interface
    cli_task = asyncio.create_task(cli_interface.start())
    
    # Wait for CLI or background tasks to complete
    try:
        await asyncio.gather(cli_task, *background_tasks, return_exceptions=True)
    except KeyboardInterrupt:
        logger.info("CLI interface interrupted")

async def launch_gui_mode(lewis_core, settings, logger, components):
    """Launch GUI interface"""
    logger.info("Launching GUI interface")
    
    gui_interface = GUIInterface(lewis_core, settings, logger)
    
    # Set up voice assistant if available
    if "voice" in components:
        voice_assistant = components["voice"]
        voice_assistant.set_command_processor(lewis_core.process_command)
        gui_interface.set_voice_assistant(voice_assistant)
    
    # Set up analytics if available
    if "analytics" in components:
        gui_interface.set_analytics_engine(components["analytics"])
    
    # Start background tasks
    background_tasks = []
    
    if "analytics" in components:
        background_tasks.append(
            asyncio.create_task(components["analytics"].start_analytics_engine())
        )
    
    if "threat_detection" in components:
        background_tasks.append(
            asyncio.create_task(components["threat_detection"].start_threat_detection())
        )
    
    # Start GUI in a separate thread since tkinter is not async
    import threading
    
    def run_gui():
        gui_interface.run()
    
    gui_thread = threading.Thread(target=run_gui, daemon=True)
    gui_thread.start()
    
    # Run background tasks
    try:
        await asyncio.gather(*background_tasks, return_exceptions=True)
    except KeyboardInterrupt:
        logger.info("GUI interface interrupted")

async def launch_server_mode(lewis_core, settings, logger, components, host, port):
    """Launch server/web interface"""
    logger.info(f"Launching server interface on {host}:{port}")
    
    web_interface = create_web_interface(lewis_core, settings, logger)
    
    # Start background tasks
    background_tasks = []
    
    if "analytics" in components:
        background_tasks.append(
            asyncio.create_task(components["analytics"].start_analytics_engine())
        )
    
    if "threat_detection" in components:
        background_tasks.append(
            asyncio.create_task(components["threat_detection"].start_threat_detection())
        )
    
    if "voice" in components:
        voice_assistant = components["voice"]
        voice_assistant.set_command_processor(lewis_core.process_command)
        background_tasks.append(
            asyncio.create_task(voice_assistant.start_voice_assistant())
        )
    
    # Start background tasks
    if background_tasks:
        for task in background_tasks:
            asyncio.create_task(task)
    
    # Start web server
    web_interface.run(host=host, port=port, debug=settings.get("debug", False))

async def shutdown_components(components):
    """Gracefully shutdown all components"""
    for name, component in components.items():
        try:
            if hasattr(component, 'stop'):
                component.stop()
            elif hasattr(component, 'shutdown'):
                await component.shutdown()
        except Exception as e:
            print(f"Error shutting down {name}: {e}")

def cli_entry():
    """CLI entry point for setup.py"""
    asyncio.run(main())

if __name__ == "__main__":
    asyncio.run(main())
