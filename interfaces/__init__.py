"""
Interfaces Module - User interface components for LEWIS.
Provides CLI, GUI, and web interfaces for system interaction.
"""

from .cli_interface import CLIInterface
from .gui_interface import GUIInterface
from .web_interface import WebInterface

__all__ = ['CLIInterface', 'GUIInterface', 'WebInterface']
