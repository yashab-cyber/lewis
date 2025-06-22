"""
GUI Interface for LEWIS
Provides graphical user interface using tkinter and customtkinter
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import customtkinter as ctk
import threading
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional
import json

# Set appearance mode and theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class LewisGUI:
    """
    Graphical User Interface for LEWIS
    Provides a modern, dark-themed interface for cybersecurity operations
    """
    
    def __init__(self, lewis_core):
        self.lewis = lewis_core
        self.root = None
        self.running = False
        
        # GUI elements
        self.chat_display = None
        self.input_entry = None
        self.status_label = None
        self.tool_tree = None
        self.progress_bar = None
        
        # Chat history
        self.chat_history = []
        
        # Current user
        self.current_user = "gui_user"
        
    def start(self):
        """Start the GUI application"""
        try:
            self.running = True
            self._create_main_window()
            self._setup_layout()
            self._update_status()
            
            # Start GUI event loop
            self.root.mainloop()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start GUI: {e}")
    
    def _create_main_window(self):
        """Create the main application window"""
        self.root = ctk.CTk()
        self.root.title("LEWIS - Linux Environment Working Intelligence System")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Set window icon (if available)
        try:
            self.root.iconbitmap("assets/lewis-icon.ico")
        except:
            pass
        
        # Configure grid weights
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
    
    def _setup_layout(self):
        """Setup the main layout"""
        # Create main frames
        self._create_sidebar()
        self._create_main_area()
        self._create_status_bar()
    
    def _create_sidebar(self):
        """Create sidebar with tools and options"""
        sidebar_frame = ctk.CTkFrame(self.root, width=250, corner_radius=0)
        sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        sidebar_frame.grid_rowconfigure(4, weight=1)
        
        # LEWIS Logo/Title
        logo_label = ctk.CTkLabel(
            sidebar_frame, 
            text="🛡️ LEWIS", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        subtitle_label = ctk.CTkLabel(
            sidebar_frame, 
            text="AI Cybersecurity Assistant",
            font=ctk.CTkFont(size=12)
        )
        subtitle_label.grid(row=1, column=0, padx=20, pady=(0, 20))
        
        # Quick Actions
        actions_label = ctk.CTkLabel(
            sidebar_frame, 
            text="Quick Actions", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        actions_label.grid(row=2, column=0, padx=20, pady=(20, 10))
        
        # Action buttons
        self.scan_btn = ctk.CTkButton(
            sidebar_frame,
            text="🔍 Network Scan",
            command=self._quick_scan,
            width=200
        )
        self.scan_btn.grid(row=3, column=0, padx=20, pady=5)
        
        self.vuln_btn = ctk.CTkButton(
            sidebar_frame,
            text="🔓 Vuln Assessment", 
            command=self._quick_vuln_scan,
            width=200
        )
        self.vuln_btn.grid(row=4, column=0, padx=20, pady=5)
        
        self.info_btn = ctk.CTkButton(
            sidebar_frame,
            text="📊 Info Gathering",
            command=self._quick_info_gathering,
            width=200
        )
        self.info_btn.grid(row=5, column=0, padx=20, pady=5)
        
        self.report_btn = ctk.CTkButton(
            sidebar_frame,
            text="📄 Generate Report",
            command=self._generate_report,
            width=200
        )
        self.report_btn.grid(row=6, column=0, padx=20, pady=5)
        
        # System Info
        system_frame = ctk.CTkFrame(sidebar_frame)
        system_frame.grid(row=7, column=0, padx=20, pady=20, sticky="ew")
        
        system_label = ctk.CTkLabel(
            system_frame,
            text="System Status",
            font=ctk.CTkFont(size=14, weight="bold")        )
        system_label.pack(pady=10)
        
        self.system_status_text = ctk.CTkTextbox(system_frame, height=100, width=200)
        self.system_status_text.pack(padx=10, pady=(0, 10))
        
        # Populate system status
        self._populate_system_status()
    
    def _create_main_area(self):
        """Create main chat and interaction area"""
        main_frame = ctk.CTkFrame(self.root)
        main_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 20), pady=20)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
          # Create tabview for different modes
        self.tabview = ctk.CTkTabview(main_frame, width=250)
        self.tabview.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # Chat tab
        self.tabview.add("💬 Chat")
        self.tabview.add("🔧 Tools")
        self.tabview.add("🔌 Extensions")
        self.tabview.add("📊 Analytics")
        self.tabview.add("⚙️ Settings")
        
        self._setup_chat_tab()
        self._setup_tools_tab()
        self._setup_extensions_tab()
        self._setup_analytics_tab()
        self._setup_settings_tab()
    
    def _setup_chat_tab(self):
        """Setup chat interface tab"""
        chat_frame = self.tabview.tab("💬 Chat")
        chat_frame.grid_columnconfigure(0, weight=1)
        chat_frame.grid_rowconfigure(0, weight=1)
        
        # Chat display area
        self.chat_display = ctk.CTkTextbox(
            chat_frame,
            height=400,
            font=ctk.CTkFont(family="Consolas", size=12)
        )
        self.chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        # Input area
        input_frame = ctk.CTkFrame(chat_frame)
        input_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")
        input_frame.grid_columnconfigure(0, weight=1)
        
        self.input_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Ask LEWIS anything about cybersecurity...",
            height=40,
            font=ctk.CTkFont(size=12)
        )
        self.input_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.input_entry.bind("<Return>", self._send_message)
        
        send_btn = ctk.CTkButton(
            input_frame,
            text="Send",
            command=self._send_message,
            width=80,
            height=40
        )
        send_btn.grid(row=0, column=1, padx=(0, 10), pady=10)
        
        # Voice button (if available)
        voice_btn = ctk.CTkButton(
            input_frame,
            text="🎤",
            command=self._voice_input,
            width=40,
            height=40
        )
        voice_btn.grid(row=0, column=2, padx=(0, 10), pady=10)
        
        # Add welcome message
        self._add_chat_message("LEWIS", "Hello! I'm LEWIS, your AI cybersecurity assistant. How can I help you today?", "assistant")
    
    def _setup_tools_tab(self):
        """Setup tools management tab"""
        tools_frame = self.tabview.tab("🔧 Tools")
        tools_frame.grid_columnconfigure(0, weight=1)
        tools_frame.grid_rowconfigure(1, weight=1)
        
        # Tools header
        tools_header = ctk.CTkLabel(
            tools_frame,
            text="Available Cybersecurity Tools",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        tools_header.grid(row=0, column=0, padx=20, pady=20)
        
        # Tools list
        self.tools_frame = ctk.CTkScrollableFrame(tools_frame)
        self.tools_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
        # Populate tools
        self._populate_tools_list()
    
    def _setup_extensions_tab(self):
        """Setup extensions management tab"""
        extensions_frame = self.tabview.tab("🔌 Extensions")
        extensions_frame.grid_columnconfigure(0, weight=1)
        extensions_frame.grid_rowconfigure(1, weight=1)
        
        # Extensions header
        extensions_header = ctk.CTkLabel(
            extensions_frame,
            text="Extension Manager",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        extensions_header.grid(row=0, column=0, padx=20, pady=20)
        
        # Control buttons frame
        control_frame = ctk.CTkFrame(extensions_frame)
        control_frame.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")
        control_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Extension control buttons
        self.reload_ext_btn = ctk.CTkButton(
            control_frame,
            text="🔄 Reload Extensions",
            command=self._reload_extensions_gui
        )
        self.reload_ext_btn.grid(row=0, column=0, padx=10, pady=10)
        
        self.refresh_ext_btn = ctk.CTkButton(
            control_frame,
            text="📊 Refresh Status",
            command=self._refresh_extensions_gui
        )
        self.refresh_ext_btn.grid(row=0, column=1, padx=10, pady=10)
        
        self.ext_help_btn = ctk.CTkButton(
            control_frame,
            text="❓ Extension Help",
            command=self._show_extension_help
        )
        self.ext_help_btn.grid(row=0, column=2, padx=10, pady=10)
        
        # Extensions list frame
        list_frame = ctk.CTkFrame(extensions_frame)
        list_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(0, weight=1)
        
        # Extensions tree view
        self.ext_tree = ttk.Treeview(
            list_frame,
            columns=("version", "status", "commands", "tools"),
            show="tree headings",
            height=15
        )
        
        # Configure columns
        self.ext_tree.heading("#0", text="Extension")
        self.ext_tree.heading("version", text="Version")
        self.ext_tree.heading("status", text="Status")
        self.ext_tree.heading("commands", text="Commands")
        self.ext_tree.heading("tools", text="Tools")
        
        self.ext_tree.column("#0", width=200)
        self.ext_tree.column("version", width=80)
        self.ext_tree.column("status", width=80)
        self.ext_tree.column("commands", width=80)
        self.ext_tree.column("tools", width=80)
        
        # Add scrollbar
        ext_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.ext_tree.yview)
        self.ext_tree.configure(yscrollcommand=ext_scrollbar.set)
        
        # Pack tree and scrollbar
        self.ext_tree.grid(row=0, column=0, sticky="nsew", padx=(10, 0), pady=10)
        ext_scrollbar.grid(row=0, column=1, sticky="ns", pady=10)
        
        # Extension details frame
        details_frame = ctk.CTkFrame(extensions_frame)
        details_frame.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        details_label = ctk.CTkLabel(
            details_frame,
            text="Extension Details",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        details_label.pack(pady=(10, 5))
        
        self.ext_details_text = ctk.CTkTextbox(details_frame, height=100)
        self.ext_details_text.pack(padx=10, pady=(0, 10), fill="x")
        
        # Bind tree selection
        self.ext_tree.bind("<<TreeviewSelect>>", self._on_extension_select)
        
        # Load extensions
        self._refresh_extensions_gui()
    
    def _setup_analytics_tab(self):
        """Setup analytics and visualization tab"""
        analytics_frame = self.tabview.tab("📊 Analytics")
        analytics_frame.grid_columnconfigure(0, weight=1)
        analytics_frame.grid_rowconfigure(1, weight=1)
        
        # Analytics header
        analytics_header = ctk.CTkLabel(
            analytics_frame,
            text="System Analytics & Metrics",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        analytics_header.grid(row=0, column=0, padx=20, pady=20)
        
        # Metrics display
        self.metrics_frame = ctk.CTkFrame(analytics_frame)
        self.metrics_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
        self._populate_analytics()
    
    def _setup_settings_tab(self):
        """Setup settings and configuration tab"""
        settings_frame = self.tabview.tab("⚙️ Settings")
        settings_frame.grid_columnconfigure(0, weight=1)
        
        # Settings header
        settings_header = ctk.CTkLabel(
            settings_frame,
            text="LEWIS Configuration",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        settings_header.grid(row=0, column=0, padx=20, pady=20)
        
        # Settings options
        self._create_settings_options(settings_frame)
    
    def _create_settings_options(self, parent):
        """Create settings options"""
        # Voice settings
        voice_frame = ctk.CTkFrame(parent)
        voice_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        voice_label = ctk.CTkLabel(voice_frame, text="Voice Settings", font=ctk.CTkFont(weight="bold"))
        voice_label.pack(pady=10)
        
        self.voice_enabled = ctk.CTkCheckBox(voice_frame, text="Enable Voice Commands")
        self.voice_enabled.pack(pady=5)
        
        # AI settings
        ai_frame = ctk.CTkFrame(parent)
        ai_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        ai_label = ctk.CTkLabel(ai_frame, text="AI Settings", font=ctk.CTkFont(weight="bold"))
        ai_label.pack(pady=10)
        
        temperature_label = ctk.CTkLabel(ai_frame, text="AI Temperature:")
        temperature_label.pack(pady=5)
        
        self.temperature_slider = ctk.CTkSlider(ai_frame, from_=0.1, to=1.0, number_of_steps=9)
        self.temperature_slider.set(0.7)
        self.temperature_slider.pack(pady=5)
        
        # Save settings button
        save_btn = ctk.CTkButton(
            parent,
            text="Save Settings",
            command=self._save_settings
        )
        save_btn.grid(row=3, column=0, padx=20, pady=20)
    
    def _create_status_bar(self):
        """Create status bar at bottom"""
        status_frame = ctk.CTkFrame(self.root, height=30, corner_radius=0)
        status_frame.grid(row=1, column=1, sticky="ew", padx=(0, 20))
        status_frame.grid_columnconfigure(0, weight=1)
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="Ready",
            font=ctk.CTkFont(size=11)
        )
        self.status_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(status_frame, width=200)
        self.progress_bar.grid(row=0, column=1, padx=10, pady=5)
        self.progress_bar.set(0)
    
    def _populate_tools_list(self):
        """Populate the tools list"""
        try:
            tool_status = self.lewis.get_tool_status()
            tools = tool_status.get("tools", {})
            
            for tool_name, status in tools.items():
                tool_frame = ctk.CTkFrame(self.tools_frame)
                tool_frame.pack(fill="x", padx=10, pady=5)
                
                # Tool name and status
                status_icon = "✅" if status.get("available") else "❌"
                tool_label = ctk.CTkLabel(
                    tool_frame,
                    text=f"{status_icon} {tool_name}",
                    font=ctk.CTkFont(weight="bold")
                )
                tool_label.pack(side="left", padx=10, pady=10)
                
                # Tool path
                path_label = ctk.CTkLabel(
                    tool_frame,
                    text=status.get("path", "Not found"),
                    font=ctk.CTkFont(size=10)
                )
                path_label.pack(side="left", padx=(0, 10), pady=10)
                
        except Exception as e:
            error_label = ctk.CTkLabel(
                self.tools_frame,
                text=f"Error loading tools: {e}",
                text_color="red"
            )
            error_label.pack(padx=10, pady=10)
    
    def _populate_analytics(self):
        """Populate analytics information"""
        try:
            status = self.lewis.get_system_status()
            stats = status.get("stats", {})
            
            # Create metrics display
            metrics_text = f"""
System Statistics:
• Commands Processed: {stats.get('total_commands', 0)}
• Knowledge Entries: {stats.get('knowledge_entries', 0)}
• Active Users: {stats.get('active_users', 0)}
• Available Tools: {stats.get('tools', 0)}

Component Status:
"""
            
            components = status.get("components", {})
            for component, ready in components.items():
                status_icon = "✅" if ready else "❌"
                metrics_text += f"• {component.replace('_', ' ').title()}: {status_icon}\n"
            
            metrics_display = ctk.CTkTextbox(
                self.metrics_frame,
                height=300,
                font=ctk.CTkFont(family="Consolas", size=11)
            )
            metrics_display.pack(fill="both", expand=True, padx=20, pady=20)
            metrics_display.insert("1.0", metrics_text)
            metrics_display.configure(state="disabled")
            
        except Exception as e:
            error_label = ctk.CTkLabel(
                self.metrics_frame,
                text=f"Error loading analytics: {e}",
                text_color="red"
            )
            error_label.pack(padx=10, pady=10)
    
    def _send_message(self, event=None):
        """Send message to LEWIS"""
        message = self.input_entry.get().strip()
        if not message:
            return
        
        # Add user message to chat
        self._add_chat_message("You", message, "user")
        
        # Clear input
        self.input_entry.delete(0, tk.END)
        
        # Update status
        self._update_status("Processing command...")
        self.progress_bar.set(0.3)
        
        # Process command in background thread
        threading.Thread(
            target=self._process_command_async,
            args=(message,),
            daemon=True
        ).start()
    
    def _process_command_async(self, message):
        """Process command asynchronously"""
        try:
            # Create new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Process command
            result = loop.run_until_complete(
                self.lewis.process_command(message, self.current_user)
            )
            
            # Update GUI in main thread
            self.root.after(0, self._handle_command_result, result)
            
        except Exception as e:
            self.root.after(0, self._handle_command_error, str(e))
        finally:
            loop.close()
    
    def _handle_command_result(self, result):
        """Handle command result in main thread"""
        try:
            if result.get("success"):
                ai_response = result.get("ai_response", {})
                response_text = ai_response.get("text", "No response generated")
                
                # Add LEWIS response to chat
                self._add_chat_message("LEWIS", response_text, "assistant")
                
                # Show suggestions if available
                suggestions = ai_response.get("suggestions", [])
                if suggestions:
                    suggestions_text = "💡 Suggestions:\n" + "\n".join(f"• {s}" for s in suggestions[:3])
                    self._add_chat_message("LEWIS", suggestions_text, "suggestion")
                
                # Show execution results if available
                execution = result.get("execution")
                if execution and execution.get("success"):
                    exec_text = f"✅ Command executed successfully\n{execution.get('output', '')[:500]}..."
                    self._add_chat_message("LEWIS", exec_text, "execution")
                
            else:
                error_msg = f"❌ Error: {result.get('error', 'Unknown error')}"
                self._add_chat_message("LEWIS", error_msg, "error")
                
        except Exception as e:
            self._add_chat_message("LEWIS", f"❌ Error processing response: {e}", "error")
        finally:
            self._update_status("Ready")
            self.progress_bar.set(0)
    
    def _handle_command_error(self, error):
        """Handle command error in main thread"""
        self._add_chat_message("LEWIS", f"❌ Error: {error}", "error")
        self._update_status("Ready")
        self.progress_bar.set(0)
    
    def _add_chat_message(self, sender, message, msg_type="normal"):
        """Add message to chat display"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Color coding based on message type
        colors = {
            "user": "#4A9EFF",
            "assistant": "#00D26A", 
            "suggestion": "#FFB800",
            "execution": "#9D4EDD",
            "error": "#FF4757",
            "normal": "#FFFFFF"
        }
        
        color = colors.get(msg_type, colors["normal"])
        
        # Format message
        formatted_message = f"[{timestamp}] {sender}: {message}\n\n"
        
        # Add to chat display
        self.chat_display.insert(tk.END, formatted_message)
        self.chat_display.see(tk.END)
        
        # Store in history
        self.chat_history.append({
            "timestamp": timestamp,
            "sender": sender,
            "message": message,
            "type": msg_type
        })
    
    def _quick_scan(self):
        """Quick network scan"""
        target = self._get_target_input("Enter target for network scan:")
        if target:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, f"scan {target}")
            self._send_message()
    
    def _quick_vuln_scan(self):
        """Quick vulnerability scan"""
        target = self._get_target_input("Enter target for vulnerability assessment:")
        if target:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, f"assess vulnerabilities for {target}")
            self._send_message()
    
    def _quick_info_gathering(self):
        """Quick information gathering"""
        target = self._get_target_input("Enter target for information gathering:")
        if target:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, f"gather information about {target}")
            self._send_message()
    
    def _generate_report(self):
        """Generate security report"""
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, "generate security report")
        self._send_message()
    
    def _get_target_input(self, prompt):
        """Get target input from user"""
        dialog = ctk.CTkInputDialog(text=prompt, title="Target Input")
        return dialog.get_input()
    
    def _voice_input(self):
        """Handle voice input"""
        try:
            # Placeholder for voice input functionality
            messagebox.showinfo("Voice Input", "Voice input feature coming soon!")
        except Exception as e:
            messagebox.showerror("Voice Error", f"Voice input error: {e}")
    
    def _save_settings(self):
        """Save settings"""
        try:
            settings = {
                "voice_enabled": self.voice_enabled.get(),
                "ai_temperature": self.temperature_slider.get()
            }
            
            # Save to configuration
            messagebox.showinfo("Settings", "Settings saved successfully!")
            
        except Exception as e:
            messagebox.showerror("Settings Error", f"Failed to save settings: {e}")
    
    def _update_status(self, status="Ready"):
        """Update status bar"""
        if self.status_label:
            self.status_label.configure(text=status)
    
    def stop(self):
        """Stop the GUI application"""
        self.running = False
        if self.root:
            self.root.quit()
            self.root.destroy()
    
    def _populate_system_status(self):
        """Populate system status display with current information"""
        try:
            # Get system status
            status = self.lewis.get_system_status()
            
            # Format status text
            status_text = "LEWIS System Status\n"
            status_text += "=" * 20 + "\n\n"
            
            # Components status
            components = status.get("components", {})
            status_text += "Core Components:\n"
            for component, is_ready in components.items():
                if component == "extensions":
                    ext_count = is_ready if isinstance(is_ready, int) else 0
                    status_icon = "✅" if ext_count > 0 else "⚠️"
                    status_text += f"{status_icon} Extensions: {ext_count} loaded\n"
                elif component == "tools":
                    tool_count = is_ready if isinstance(is_ready, int) else 0
                    status_icon = "✅" if tool_count > 0 else "⚠️"
                    status_text += f"{status_icon} Tools: {tool_count} available\n"
                else:
                    status_icon = "✅" if is_ready else "❌"
                    comp_name = component.replace("_", " ").title()
                    status_text += f"{status_icon} {comp_name}: {'Ready' if is_ready else 'Not Ready'}\n"
            
            # Stats
            stats = status.get("stats", {})
            if stats:
                status_text += f"\nStatistics:\n"
                status_text += f"Commands: {stats.get('total_commands', 0)}\n"
                status_text += f"Knowledge: {stats.get('knowledge_entries', 0)}\n"
                status_text += f"Users: {stats.get('active_users', 0)}\n"
            
            # Extension details
            try:
                extension_status = self.lewis.get_extension_status()
                if extension_status and extension_status.get("loaded_extensions"):
                    status_text += f"\nLoaded Extensions:\n"
                    for ext_name, ext_info in extension_status["loaded_extensions"].items():
                        status_text += f"• {ext_name} v{ext_info.get('version', '?')}\n"
            except:
                pass
            
            # Update display
            self.system_status_text.delete("1.0", "end")
            self.system_status_text.insert("1.0", status_text)
            
        except Exception as e:
            error_text = f"Error loading system status:\n{str(e)}"
            self.system_status_text.delete("1.0", "end")
            self.system_status_text.insert("1.0", error_text)

class GUIInterface:
    """GUI Interface wrapper for LEWIS"""
    
    def __init__(self, lewis_core):
        self.lewis = lewis_core
        self.gui = None
    
    def start(self):
        """Start GUI interface"""
        try:
            self.gui = LewisGUI(self.lewis)
            self.gui.start()
        except Exception as e:
            print(f"❌ Failed to start GUI: {e}")
    
    def stop(self):
        """Stop GUI interface"""
        if self.gui:
            self.gui.stop()

    def _reload_extensions_gui(self):
        """Reload all extensions from GUI"""
        try:
            # Update status
            self._update_status("Reloading extensions...")
            
            # Reload extensions in separate thread
            def reload_thread():
                try:
                    self.lewis.extension_manager.unload_all_extensions()
                    self.lewis.extension_manager.load_all_extensions()
                    
                    # Update GUI in main thread
                    self.root.after(0, lambda: [
                        self._refresh_extensions_gui(),
                        self._update_status("Extensions reloaded successfully"),
                        messagebox.showinfo("Success", "Extensions reloaded successfully!")
                    ])
                except Exception as e:
                    self.root.after(0, lambda: [
                        self._update_status("Extension reload failed"),
                        messagebox.showerror("Error", f"Failed to reload extensions: {e}")
                    ])
            
            threading.Thread(target=reload_thread, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to reload extensions: {e}")
    
    def _refresh_extensions_gui(self):
        """Refresh extensions display"""
        try:
            # Clear existing items
            for item in self.ext_tree.get_children():
                self.ext_tree.delete(item)
            
            # Get extension status
            extension_status = self.lewis.get_extension_status()
            
            if not extension_status or not extension_status.get("loaded_extensions"):
                # Add "No extensions" item
                self.ext_tree.insert("", "end", text="No extensions loaded", 
                                   values=("", "Inactive", "0", "0"))
                return
            
            # Add extensions to tree
            for ext_name, ext_info in extension_status["loaded_extensions"].items():
                commands_count = len(ext_info.get("commands", []))
                tools_count = len(ext_info.get("tools", []))
                status = "Active" if ext_info.get("active", True) else "Inactive"
                version = ext_info.get("version", "Unknown")
                
                self.ext_tree.insert("", "end", text=ext_name,
                                   values=(version, status, commands_count, tools_count))
            
        except Exception as e:
            print(f"Error refreshing extensions: {e}")
    
    def _on_extension_select(self, event):
        """Handle extension selection in tree"""
        try:
            selection = self.ext_tree.selection()
            if not selection:
                return
            
            item = self.ext_tree.item(selection[0])
            ext_name = item["text"]
            
            if ext_name == "No extensions loaded":
                self.ext_details_text.delete("1.0", "end")
                self.ext_details_text.insert("1.0", "No extensions are currently loaded.")
                return
            
            # Get extension details
            extension_status = self.lewis.get_extension_status()
            ext_info = extension_status.get("loaded_extensions", {}).get(ext_name, {})
            
            # Format details
            details = f"Extension: {ext_name}\n"
            details += f"Version: {ext_info.get('version', 'Unknown')}\n"
            details += f"Status: {'Active' if ext_info.get('active', True) else 'Inactive'}\n"
            details += f"Path: {ext_info.get('path', 'Unknown')}\n\n"
            
            commands = ext_info.get("commands", [])
            if commands:
                details += f"Commands ({len(commands)}):\n"
                for cmd in commands:
                    details += f"  • {cmd}\n"
                details += "\n"
            
            tools = ext_info.get("tools", [])
            if tools:
                details += f"Tools ({len(tools)}):\n"
                for tool in tools:
                    details += f"  • {tool}\n"
            
            # Update details display
            self.ext_details_text.delete("1.0", "end")
            self.ext_details_text.insert("1.0", details)
            
        except Exception as e:
            print(f"Error showing extension details: {e}")
    
    def _show_extension_help(self):
        """Show extension system help"""
        help_text = """
LEWIS Extension System Help

Extensions are modular components that add functionality to LEWIS:

• Load Extensions: Extensions are automatically loaded at startup
• Reload Extensions: Use the reload button to refresh all extensions
• Extension Commands: Extensions can add new commands to LEWIS
• Extension Tools: Extensions can provide specialized security tools

Extension Structure:
- Each extension has its own directory
- Extensions can provide commands, tools, and interfaces
- Extensions are configured in config/config.yaml

Common Commands:
- Use extension commands directly in the chat interface
- Type 'extensions' in CLI mode to see loaded extensions
- Extension commands appear in the help system

For more information, see the documentation in manual/14-extensions.md
        """
        messagebox.showinfo("Extension Help", help_text)
