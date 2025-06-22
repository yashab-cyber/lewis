"""
Logger utility for LEWIS
Provides structured logging with different levels and formats
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from loguru import logger
import colorama
from colorama import Fore, Style

# Initialize colorama for Windows
colorama.init()

class Logger:
    """Enhanced logger for LEWIS with color support and structured output"""
    
    def __init__(self, name: str = "LEWIS", level: str = "INFO"):
        self.name = name
        self.level = level
        self._setup_logger()
    
    def _setup_logger(self):
        """Setup logger configuration"""
        # Remove default handler
        logger.remove()
        
        # Add console handler with colors
        logger.add(
            sys.stderr,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                   "<level>{level: <8}</level> | "
                   "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
                   "<level>{message}</level>",
            level=self.level,
            colorize=True
        )
        
        # Add file handler
        log_file = Path("logs") / "lewis.log"
        log_file.parent.mkdir(exist_ok=True)
        
        logger.add(
            log_file,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
            level="DEBUG",
            rotation="10 MB",
            retention="7 days",
            compression="zip"
        )
    
    def info(self, message: str):
        """Log info message"""
        logger.info(message)
    
    def debug(self, message: str):
        """Log debug message"""
        logger.debug(message)
    
    def warning(self, message: str):
        """Log warning message"""
        logger.warning(message)
    
    def error(self, message: str):
        """Log error message"""
        logger.error(message)
    
    def critical(self, message: str):
        """Log critical message"""
        logger.critical(message)
    
    def success(self, message: str):
        """Log success message"""
        logger.success(message)

def setup_logger(debug: bool = False) -> Logger:
    """Setup and return logger instance"""
    level = "DEBUG" if debug else "INFO"
    return Logger(level=level)


class ColorFormatter:
    """Color formatter for console output"""
    
    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.MAGENTA,
        'SUCCESS': Fore.GREEN
    }
    
    @classmethod
    def format_message(cls, level: str, message: str) -> str:
        """Format message with colors"""
        color = cls.COLORS.get(level, Fore.WHITE)
        return f"{color}{message}{Style.RESET_ALL}"
