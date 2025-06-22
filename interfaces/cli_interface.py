"""
CLI Interface for LEWIS
Provides command-line interface with optional voice support
"""

import asyncio
import sys
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.table import Table
from rich.live import Live
from rich.spinner import Spinner

try:
    import speech_recognition as sr
    import pyttsx3
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False

class CLIInterface:
    """
    Command Line Interface for LEWIS
    Provides interactive chat interface with optional voice support
    """
    
    def __init__(self, lewis_core, voice_enabled: bool = False):
        self.lewis = lewis_core
        self.console = Console()
        self.voice_enabled = voice_enabled and VOICE_AVAILABLE
        
        # Initialize voice components
        if self.voice_enabled:
            self._initialize_voice()
        
        # User session
        self.user_id = "cli_user"
        self.session_active = True
        
    def _initialize_voice(self):
        """Initialize voice recognition and synthesis"""
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            self.tts_engine = pyttsx3.init()
            
            # Configure TTS
            self.tts_engine.setProperty('rate', 150)
            self.tts_engine.setProperty('volume', 0.8)
            
            # Adjust for ambient noise
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
            self.console.print("🎤 Voice interface initialized", style="green")
            
        except Exception as e:
            self.console.print(f"⚠️  Voice initialization failed: {e}", style="yellow")
            self.voice_enabled = False
    
    def start(self):
        """Start the CLI interface"""
        try:
            self._display_welcome()
            self._start_interactive_session()
            
        except KeyboardInterrupt:
            self._display_goodbye()
        except Exception as e:
            self.console.print(f"❌ CLI Error: {e}", style="red")
    
    def _display_welcome(self):
        """Display welcome message and system info"""
        # ASCII Art for LEWIS
        ascii_art = """
        ██╗     ███████╗██╗    ██╗██╗███████╗
        ██║     ██╔════╝██║    ██║██║██╔════╝
        ██║     █████╗  ██║ █╗ ██║██║███████╗
        ██║     ██╔══╝  ██║███╗██║██║╚════██║
        ███████╗███████╗╚███╔███╔╝██║███████║
        ╚══════╝╚══════╝ ╚══╝╚══╝ ╚═╝╚══════╝
        """
        
        welcome_text = Text()
        welcome_text.append("Linux Environment Working Intelligence System\n", style="bold cyan")
        welcome_text.append("AI-Powered Cybersecurity Assistant", style="italic blue")
        
        panel = Panel(
            welcome_text,
            title="🚀 LEWIS v1.0",
            border_style="cyan",
            padding=(1, 2)
        )
        
        self.console.print(ascii_art, style="cyan")
        self.console.print(panel)
        
        # Display system status
        self._display_system_status()
        
        # Display available commands
        self._display_help()
        
    def _display_system_status(self):
        """Display current system status"""
        status = self.lewis.get_system_status()
        
        status_table = Table(title="System Status", show_header=True, header_style="bold magenta")
        status_table.add_column("Component", style="cyan")
        status_table.add_column("Status", style="green")
        status_table.add_column("Details", style="white")
        
        components = status.get("components", {})
        for component, is_ready in components.items():
            status_emoji = "✅" if is_ready else "❌"
            status_text = "Ready" if is_ready else "Not Ready"
            
            # Add details for specific components
            details = ""
            if component == "extensions":
                extension_count = is_ready if isinstance(is_ready, int) else 0
                details = f"{extension_count} loaded"
                is_ready = extension_count > 0
                status_emoji = "✅" if is_ready else "⚠️"
                status_text = f"{extension_count} Extensions" if extension_count > 0 else "No Extensions"
            elif component == "tools":
                tool_count = is_ready if isinstance(is_ready, int) else 0
                details = f"{tool_count} available"
                status_text = f"{tool_count} Tools" if tool_count > 0 else "No Tools"
            
            status_table.add_row(
                component.replace("_", " ").title(), 
                f"{status_emoji} {status_text}",
                details
            )
        
        self.console.print(status_table)
        
        # Display extension status if available
        try:
            extension_status = self.lewis.get_extension_status()
            if extension_status and extension_status.get("loaded_extensions"):
                ext_table = Table(title="Loaded Extensions", show_header=True, header_style="bold blue")
                ext_table.add_column("Extension", style="yellow")
                ext_table.add_column("Version", style="cyan")
                ext_table.add_column("Commands", style="green")
                
                for ext_name, ext_info in extension_status["loaded_extensions"].items():
                    commands = ext_info.get("commands", [])
                    command_count = len(commands) if commands else 0
                    ext_table.add_row(
                        ext_name,
                        ext_info.get("version", "Unknown"),
                        str(command_count)
                    )
                
                self.console.print(ext_table)
        except:
            pass  # Extension status not available
        
        self.console.print()
        
    def _display_help(self):
        """Display available commands and help"""
        help_table = Table(title="Core Commands", show_header=True, header_style="bold blue")
        help_table.add_column("Command", style="yellow")
        help_table.add_column("Description", style="white")
        
        commands = [
            ("scan <target>", "Perform network scan"),
            ("vuln <target>", "Vulnerability assessment"),
            ("info <target>", "Gather information"),
            ("report", "Generate security report"),
            ("help", "Show this help message"),
            ("extensions", "List loaded extensions"),
            ("reload-extensions", "Reload all extensions"),
            ("voice", "Toggle voice mode (if available)"),
            ("status", "Show system status"),
            ("exit/quit", "Exit LEWIS")
        ]
        
        for cmd, desc in commands:
            help_table.add_row(cmd, desc)
        
        if self.voice_enabled:
            help_table.add_row("voice input", "Say 'Lewis' followed by your command")
        
        self.console.print(help_table)
        
        # Display extension commands if available
        try:
            available_commands = self.lewis.get_available_commands()
            extension_commands = {
                cmd: desc for cmd, desc in available_commands.items()
                if "extension" in desc.lower() or cmd not in [c[0].split()[0] for c in commands]
            }
            
            if extension_commands:
                ext_help_table = Table(title="Extension Commands", show_header=True, header_style="bold green")
                ext_help_table.add_column("Command", style="yellow")
                ext_help_table.add_column("Description", style="white")
                
                for cmd, desc in extension_commands.items():
                    ext_help_table.add_row(cmd, desc)
                
                self.console.print(ext_help_table)
        except:
            pass  # Extension commands not available
        
        self.console.print()
    
    def _start_interactive_session(self):
        """Start interactive command session"""
        self.console.print("💬 Ready for commands. Type 'help' for assistance or 'exit' to quit.\n")
        
        while self.session_active:
            try:
                # Get user input
                user_input = self._get_user_input()
                
                if not user_input:
                    continue
                
                # Handle special commands
                if self._handle_special_commands(user_input):
                    continue
                
                # Process command through LEWIS
                self._process_command(user_input)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                self.console.print(f"❌ Error: {e}", style="red")
    
    def _get_user_input(self) -> str:
        """Get user input via text or voice"""
        if self.voice_enabled:
            mode_indicator = "🎤/💬"
        else:
            mode_indicator = "💬"
        
        try:
            # Check for voice input first if enabled
            if self.voice_enabled and self._check_for_voice_activation():
                return self._get_voice_input()
            
            # Get text input
            return Prompt.ask(f"[bold cyan]{mode_indicator} LEWIS[/bold cyan]", default="")
            
        except (EOFError, KeyboardInterrupt):
            return "exit"
    
    def _check_for_voice_activation(self) -> bool:
        """Check if user wants to use voice input"""
        # This could be enhanced to listen for wake word
        return False  # Simplified for now
    
    def _get_voice_input(self) -> str:
        """Get voice input from user"""
        try:
            self.console.print("🎤 Listening... (speak now)", style="yellow")
            
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            self.console.print("🔄 Processing speech...", style="blue")
            text = self.recognizer.recognize_google(audio)
            
            self.console.print(f"🎤 You said: [italic]{text}[/italic]")
            return text
            
        except sr.WaitTimeoutError:
            self.console.print("⏰ No speech detected", style="yellow")
            return ""
        except sr.UnknownValueError:
            self.console.print("❓ Could not understand speech", style="yellow")
            return ""
        except Exception as e:
            self.console.print(f"🎤 Voice input error: {e}", style="red")
            return ""
    
    def _handle_special_commands(self, user_input: str) -> bool:
        """Handle special CLI commands"""
        cmd = user_input.lower().strip()
        
        if cmd in ["exit", "quit", "bye"]:
            self.session_active = False
            return True
        
        elif cmd == "help":
            self._display_help()
            return True
        
        elif cmd == "status":
            self._display_system_status()
            return True
        
        elif cmd == "extensions":
            self._display_extensions()
            return True
        
        elif cmd == "reload-extensions":
            self._reload_extensions()
            return True
        
        elif cmd == "voice":
            if VOICE_AVAILABLE:
                self.voice_enabled = not self.voice_enabled
                status = "enabled" if self.voice_enabled else "disabled"
                self.console.print(f"🎤 Voice mode {status}", style="green")
                if self.voice_enabled and not hasattr(self, 'recognizer'):
                    self._initialize_voice()
            else:
                self.console.print("🎤 Voice features not available (missing dependencies)", style="yellow")
            return True
        
        elif cmd == "clear":
            self.console.clear()
            return True
        
        return False
    
    def _process_command(self, user_input: str):
        """Process user command through LEWIS"""
        # Show processing indicator
        with Live(Spinner("dots", text="Processing..."), console=self.console):
            # Run async command processing
            result = asyncio.run(self.lewis.process_command(user_input, self.user_id))
        
        # Display result
        self._display_result(result)
    
    def _display_result(self, result: dict):
        """Display command result"""
        if not result.get("success"):
            self.console.print(f"❌ Error: {result.get('error', 'Unknown error')}", style="red")
            return
        
        # Display AI response
        ai_response = result.get("ai_response", {})
        response_text = ai_response.get("text", "No response generated")
        
        # Create response panel
        response_panel = Panel(
            response_text,
            title="🤖 LEWIS Response",
            border_style="green",
            padding=(1, 2)
        )
        self.console.print(response_panel)
        
        # Speak response if voice is enabled
        if self.voice_enabled and response_text:
            self._speak_response(response_text)
        
        # Display suggestions if available
        suggestions = ai_response.get("suggestions", [])
        if suggestions:
            self._display_suggestions(suggestions)
        
        # Display execution results if available
        execution = result.get("execution")
        if execution:
            self._display_execution_result(execution)
    
    def _display_suggestions(self, suggestions: list):
        """Display command suggestions"""
        if not suggestions:
            return
            
        suggestion_table = Table(title="💡 Suggestions", show_header=False)
        suggestion_table.add_column("Command", style="cyan")
        
        for suggestion in suggestions[:5]:  # Show max 5 suggestions
            suggestion_table.add_row(f"• {suggestion}")
        
        self.console.print(suggestion_table)
    
    def _display_execution_result(self, execution: dict):
        """Display command execution results"""
        if execution.get("success"):
            self.console.print("✅ Command executed successfully", style="green")
            
            output = execution.get("output", "")
            if output:
                output_panel = Panel(
                    output[:1000] + ("..." if len(output) > 1000 else ""),
                    title="📋 Command Output",
                    border_style="blue"
                )
                self.console.print(output_panel)
        else:
            error = execution.get("error", "Unknown execution error")
            self.console.print(f"❌ Execution failed: {error}", style="red")
    
    def _speak_response(self, text: str):
        """Speak the response using TTS"""
        try:
            # Clean text for TTS
            clean_text = text.replace("🤖", "").replace("✅", "").replace("❌", "")
            clean_text = clean_text[:200]  # Limit length
            
            self.tts_engine.say(clean_text)
            self.tts_engine.runAndWait()
            
        except Exception as e:
            self.console.print(f"🔊 TTS Error: {e}", style="yellow")
    
    def _display_goodbye(self):
        """Display goodbye message"""
        goodbye_panel = Panel(
            "Thank you for using LEWIS!\nStay secure! 🛡️",
            title="👋 Goodbye",
            border_style="cyan"
        )
        self.console.print(goodbye_panel)
    
    def _display_extensions(self):
        """Display detailed extension information"""
        try:
            extension_status = self.lewis.get_extension_status()
            
            if not extension_status or not extension_status.get("loaded_extensions"):
                self.console.print("📦 No extensions loaded", style="yellow")
                return
            
            # Extension overview
            overview_table = Table(title="Extension Overview", show_header=True, header_style="bold cyan")
            overview_table.add_column("Metric", style="yellow")
            overview_table.add_column("Value", style="white")
            
            total_extensions = len(extension_status["loaded_extensions"])
            total_commands = sum(len(ext.get("commands", [])) for ext in extension_status["loaded_extensions"].values())
            total_tools = sum(len(ext.get("tools", [])) for ext in extension_status["loaded_extensions"].values())
            
            overview_table.add_row("Total Extensions", str(total_extensions))
            overview_table.add_row("Total Commands", str(total_commands))
            overview_table.add_row("Total Tools", str(total_tools))
            
            self.console.print(overview_table)
            self.console.print()
            
            # Detailed extension list
            ext_table = Table(title="Loaded Extensions", show_header=True, header_style="bold green")
            ext_table.add_column("Extension", style="yellow")
            ext_table.add_column("Version", style="cyan")
            ext_table.add_column("Status", style="green")
            ext_table.add_column("Commands", style="blue")
            ext_table.add_column("Tools", style="magenta")
            
            for ext_name, ext_info in extension_status["loaded_extensions"].items():
                commands = ext_info.get("commands", [])
                tools = ext_info.get("tools", [])
                status = "✅ Active" if ext_info.get("active", True) else "❌ Inactive"
                
                ext_table.add_row(
                    ext_name,
                    ext_info.get("version", "Unknown"),
                    status,
                    str(len(commands)),
                    str(len(tools))
                )
            
            self.console.print(ext_table)
            
            # Show available extension commands
            available_commands = self.lewis.get_available_commands()
            extension_commands = {
                cmd: desc for cmd, desc in available_commands.items()
                if any(cmd in ext.get("commands", []) for ext in extension_status["loaded_extensions"].values())
            }
            
            if extension_commands:
                self.console.print()
                cmd_table = Table(title="Available Extension Commands", show_header=True, header_style="bold blue")
                cmd_table.add_column("Command", style="yellow")
                cmd_table.add_column("Description", style="white")
                
                for cmd, desc in extension_commands.items():
                    cmd_table.add_row(cmd, desc)
                
                self.console.print(cmd_table)
            
        except Exception as e:
            self.console.print(f"❌ Error displaying extensions: {e}", style="red")
    
    def _reload_extensions(self):
        """Reload all extensions"""
        try:
            self.console.print("🔄 Reloading extensions...", style="blue")
            
            # Unload all extensions
            self.lewis.extension_manager.unload_all_extensions()
            
            # Load all extensions
            self.lewis.extension_manager.load_all_extensions()
            
            # Get new status
            extension_status = self.lewis.get_extension_status()
            loaded_count = len(extension_status.get("loaded_extensions", {}))
            
            self.console.print(f"✅ Extensions reloaded successfully! {loaded_count} extensions loaded", style="green")
            
        except Exception as e:
            self.console.print(f"❌ Error reloading extensions: {e}", style="red")
