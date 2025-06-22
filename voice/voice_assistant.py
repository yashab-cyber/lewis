#!/usr/bin/env python3
"""
LEWIS Voice Assistant Framework
Speech recognition, text-to-speech, and voice command processing
"""

import asyncio
import json
import threading
import queue
import time
from datetime import datetime
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
import tempfile
import os

# Speech recognition libraries
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False

# Text-to-speech libraries
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False

# Alternative TTS with gTTS
try:
    from gtts import gTTS
    import pygame
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

# Wake word detection
try:
    import pvporcupine
    PORCUPINE_AVAILABLE = True
except ImportError:
    PORCUPINE_AVAILABLE = False

# Audio processing
try:
    import pyaudio
    import wave
    import audioop
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False

from config.settings import Settings
from utils.logger import Logger

@dataclass
class VoiceCommand:
    command: str
    confidence: float
    timestamp: datetime
    user_id: str
    session_id: str = None

@dataclass
class VoiceResponse:
    text: str
    audio_data: bytes = None
    timestamp: datetime = None

class VoiceAssistant:
    """Comprehensive voice assistant for LEWIS"""
    
    def __init__(self, settings: Settings, logger: Logger):
        self.settings = settings
        self.logger = logger
        
        # Voice configuration
        self.voice_config = settings.get("voice", {})
        self.enabled = self.voice_config.get("enabled", False)
        self.wake_word = self.voice_config.get("wake_word", "lewis")
        self.language = self.voice_config.get("language", "en")
        self.voice_rate = self.voice_config.get("rate", 150)
        self.voice_volume = self.voice_config.get("volume", 0.9)
        
        # Audio settings
        self.sample_rate = 16000
        self.chunk_size = 1024
        self.channels = 1
        self.format = pyaudio.paInt16 if AUDIO_AVAILABLE else None
        
        # Initialize components
        self.recognizer = None
        self.microphone = None
        self.tts_engine = None
        self.wake_word_detector = None
        
        # State management
        self.is_listening = False
        self.is_speaking = False
        self.wake_word_detected = False
        
        # Command processing
        self.command_queue = queue.Queue()
        self.response_queue = queue.Queue()
        self.command_processor = None
        
        # Initialize voice components
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize voice recognition and synthesis components"""
        
        if not self.enabled:
            self.logger.info("Voice assistant is disabled")
            return
        
        try:
            # Initialize speech recognition
            if SPEECH_RECOGNITION_AVAILABLE:
                self.recognizer = sr.Recognizer()
                self.recognizer.energy_threshold = 300
                self.recognizer.pause_threshold = 1.0
                self.recognizer.phrase_threshold = 0.3
                
                if AUDIO_AVAILABLE:
                    self.microphone = sr.Microphone()
                    # Adjust for ambient noise
                    with self.microphone as source:
                        self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                self.logger.info("Speech recognition initialized")
            else:
                self.logger.warning("Speech recognition not available")
            
            # Initialize text-to-speech
            if PYTTSX3_AVAILABLE:
                self.tts_engine = pyttsx3.init()
                self.tts_engine.setProperty('rate', self.voice_rate)
                self.tts_engine.setProperty('volume', self.voice_volume)
                
                # Set voice (prefer female voice if available)
                voices = self.tts_engine.getProperty('voices')
                if voices:
                    for voice in voices:
                        if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                            self.tts_engine.setProperty('voice', voice.id)
                            break
                
                self.logger.info("Text-to-speech initialized")
            else:
                self.logger.warning("Text-to-speech not available")
            
            # Initialize wake word detection
            if PORCUPINE_AVAILABLE:
                try:
                    self.wake_word_detector = pvporcupine.create(
                        keywords=[self.wake_word]
                    )
                    self.logger.info(f"Wake word detection initialized for '{self.wake_word}'")
                except:
                    self.logger.warning("Wake word detection failed to initialize")
            
        except Exception as e:
            self.logger.error(f"Voice assistant initialization failed: {str(e)}")
    
    def set_command_processor(self, processor: Callable):
        """Set the command processor function"""
        self.command_processor = processor
    
    async def start_voice_assistant(self):
        """Start the voice assistant"""
        
        if not self.enabled or not SPEECH_RECOGNITION_AVAILABLE:
            self.logger.info("Voice assistant not started (disabled or components unavailable)")
            return
        
        self.logger.info("Starting voice assistant")
        
        # Start voice processing tasks
        tasks = [
            asyncio.create_task(self._listen_for_wake_word()),
            asyncio.create_task(self._process_voice_commands()),
            asyncio.create_task(self._handle_responses())
        ]
        
        await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _listen_for_wake_word(self):
        """Listen for wake word in background"""
        
        while True:
            try:
                if not self.is_listening and not self.is_speaking:
                    # Listen for wake word
                    if await self._detect_wake_word():
                        self.wake_word_detected = True
                        self.logger.info("Wake word detected")
                        
                        # Start listening for command
                        await self._listen_for_command()
                
                await asyncio.sleep(0.1)  # Small delay to prevent excessive CPU usage
                
            except Exception as e:
                self.logger.error(f"Wake word detection error: {str(e)}")
                await asyncio.sleep(1)
    
    async def _detect_wake_word(self) -> bool:
        """Detect wake word using available methods"""
        
        try:
            if self.wake_word_detector and AUDIO_AVAILABLE:
                # Use Porcupine for wake word detection
                return await self._porcupine_wake_word_detection()
            else:
                # Fallback to continuous listening with speech recognition
                return await self._fallback_wake_word_detection()
        
        except Exception as e:
            self.logger.error(f"Wake word detection failed: {str(e)}")
            return False
    
    async def _porcupine_wake_word_detection(self) -> bool:
        """Use Porcupine for wake word detection"""
        
        try:
            audio = pyaudio.PyAudio()
            stream = audio.open(
                rate=self.wake_word_detector.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.wake_word_detector.frame_length
            )
            
            # Listen for a short period
            for _ in range(10):  # Check for 10 frames
                pcm = stream.read(self.wake_word_detector.frame_length)
                pcm = [int.from_bytes(pcm[i:i+2], byteorder='little', signed=True) 
                       for i in range(0, len(pcm), 2)]
                
                keyword_index = self.wake_word_detector.process(pcm)
                if keyword_index >= 0:
                    stream.close()
                    audio.terminate()
                    return True
            
            stream.close()
            audio.terminate()
            return False
            
        except Exception as e:
            self.logger.error(f"Porcupine wake word detection error: {str(e)}")
            return False
    
    async def _fallback_wake_word_detection(self) -> bool:
        """Fallback wake word detection using speech recognition"""
        
        try:
            with self.microphone as source:
                # Listen for short audio
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=2)
            
            # Recognize speech
            text = self.recognizer.recognize_google(audio, language=self.language).lower()
            
            # Check for wake word
            return self.wake_word.lower() in text
            
        except sr.WaitTimeoutError:
            return False
        except sr.UnknownValueError:
            return False
        except Exception as e:
            self.logger.debug(f"Wake word detection error: {str(e)}")
            return False
    
    async def _listen_for_command(self):
        """Listen for voice command after wake word"""
        
        try:
            self.is_listening = True
            
            # Play acknowledgment sound or speak
            await self.speak("Yes?")
            
            # Listen for command
            command = await self._capture_voice_command()
            
            if command:
                # Add to command queue
                voice_command = VoiceCommand(
                    command=command,
                    confidence=0.8,  # Placeholder
                    timestamp=datetime.now(),
                    user_id="voice_user"
                )
                
                self.command_queue.put(voice_command)
                self.logger.info(f"Voice command received: {command}")
            
        except Exception as e:
            self.logger.error(f"Command listening error: {str(e)}")
        
        finally:
            self.is_listening = False
            self.wake_word_detected = False
    
    async def _capture_voice_command(self) -> Optional[str]:
        """Capture and recognize voice command"""
        
        try:
            with self.microphone as source:
                self.logger.info("Listening for command...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            # Recognize speech
            command = self.recognizer.recognize_google(audio, language=self.language)
            return command
            
        except sr.WaitTimeoutError:
            await self.speak("I didn't hear anything. Please try again.")
            return None
        except sr.UnknownValueError:
            await self.speak("I couldn't understand that. Please repeat.")
            return None
        except Exception as e:
            self.logger.error(f"Voice command capture error: {str(e)}")
            await self.speak("Sorry, there was an error processing your command.")
            return None
    
    async def _process_voice_commands(self):
        """Process voice commands from queue"""
        
        while True:
            try:
                if not self.command_queue.empty():
                    voice_command = self.command_queue.get()
                    
                    # Process command if processor is available
                    if self.command_processor:
                        try:
                            # Process command asynchronously
                            result = await self.command_processor(
                                voice_command.command,
                                voice_command.user_id
                            )
                            
                            # Generate response
                            response_text = self._generate_voice_response(result)
                            
                            # Add to response queue
                            response = VoiceResponse(
                                text=response_text,
                                timestamp=datetime.now()
                            )
                            
                            self.response_queue.put(response)
                            
                        except Exception as e:
                            self.logger.error(f"Command processing error: {str(e)}")
                            error_response = VoiceResponse(
                                text="Sorry, I encountered an error processing your command.",
                                timestamp=datetime.now()
                            )
                            self.response_queue.put(error_response)
                    
                    self.command_queue.task_done()
                
                await asyncio.sleep(0.1)
                
            except Exception as e:
                self.logger.error(f"Voice command processing error: {str(e)}")
                await asyncio.sleep(1)
    
    async def _handle_responses(self):
        """Handle voice responses from queue"""
        
        while True:
            try:
                if not self.response_queue.empty():
                    response = self.response_queue.get()
                    
                    # Speak the response
                    await self.speak(response.text)
                    
                    self.response_queue.task_done()
                
                await asyncio.sleep(0.1)
                
            except Exception as e:
                self.logger.error(f"Response handling error: {str(e)}")
                await asyncio.sleep(1)
    
    def _generate_voice_response(self, command_result: Dict[str, Any]) -> str:
        """Generate appropriate voice response from command result"""
        
        try:
            if command_result.get("success"):
                output = command_result.get("output", "")
                
                # Summarize long outputs for voice
                if len(output) > 200:
                    # Extract key information
                    lines = output.split('\n')
                    important_lines = [line for line in lines if any(keyword in line.lower() 
                                     for keyword in ['found', 'discovered', 'detected', 'error', 'warning', 'open', 'closed'])]
                    
                    if important_lines:
                        summary = "Here are the key findings: " + ". ".join(important_lines[:3])
                    else:
                        summary = "Command completed successfully. Check the detailed output for more information."
                    
                    return summary
                else:
                    return f"Command completed. {output}"
            else:
                error = command_result.get("error", "Unknown error occurred")
                return f"Command failed: {error}"
                
        except Exception as e:
            self.logger.error(f"Response generation error: {str(e)}")
            return "I encountered an error generating the response."
    
    async def speak(self, text: str):
        """Convert text to speech and play"""
        
        if not text or self.is_speaking:
            return
        
        try:
            self.is_speaking = True
            self.logger.info(f"Speaking: {text}")
            
            if PYTTSX3_AVAILABLE and self.tts_engine:
                # Use pyttsx3 for TTS
                await self._speak_with_pyttsx3(text)
            elif GTTS_AVAILABLE:
                # Use gTTS as fallback
                await self._speak_with_gtts(text)
            else:
                self.logger.warning("No TTS engine available")
            
        except Exception as e:
            self.logger.error(f"Text-to-speech error: {str(e)}")
        
        finally:
            self.is_speaking = False
    
    async def _speak_with_pyttsx3(self, text: str):
        """Speak using pyttsx3"""
        
        def speak_sync():
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        
        # Run in thread to avoid blocking
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, speak_sync)
    
    async def _speak_with_gtts(self, text: str):
        """Speak using gTTS"""
        
        try:
            # Generate speech
            tts = gTTS(text=text, lang=self.language[:2], slow=False)
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                tts.save(tmp_file.name)
                tmp_path = tmp_file.name
            
            # Play audio
            pygame.mixer.init()
            pygame.mixer.music.load(tmp_path)
            pygame.mixer.music.play()
            
            # Wait for playback to complete
            while pygame.mixer.music.get_busy():
                await asyncio.sleep(0.1)
            
            # Clean up
            os.unlink(tmp_path)
            
        except Exception as e:
            self.logger.error(f"gTTS speech error: {str(e)}")
    
    async def process_voice_input(self, audio_data: bytes) -> Optional[str]:
        """Process raw audio input and return recognized text"""
        
        if not SPEECH_RECOGNITION_AVAILABLE:
            return None
        
        try:
            # Convert audio data to AudioData object
            audio = sr.AudioData(audio_data, self.sample_rate, 2)
            
            # Recognize speech
            text = self.recognizer.recognize_google(audio, language=self.language)
            return text
            
        except sr.UnknownValueError:
            return None
        except Exception as e:
            self.logger.error(f"Voice input processing error: {str(e)}")
            return None
    
    def is_voice_available(self) -> bool:
        """Check if voice capabilities are available"""
        return (SPEECH_RECOGNITION_AVAILABLE and AUDIO_AVAILABLE and 
                (PYTTSX3_AVAILABLE or GTTS_AVAILABLE))
    
    def get_voice_status(self) -> Dict[str, Any]:
        """Get current voice assistant status"""
        
        return {
            "enabled": self.enabled,
            "available": self.is_voice_available(),
            "is_listening": self.is_listening,
            "is_speaking": self.is_speaking,
            "wake_word": self.wake_word,
            "language": self.language,
            "components": {
                "speech_recognition": SPEECH_RECOGNITION_AVAILABLE,
                "text_to_speech": PYTTSX3_AVAILABLE or GTTS_AVAILABLE,
                "wake_word_detection": PORCUPINE_AVAILABLE,
                "audio_processing": AUDIO_AVAILABLE
            }
        }
    
    def stop_voice_assistant(self):
        """Stop the voice assistant"""
        
        self.enabled = False
        self.is_listening = False
        self.is_speaking = False
        
        if self.tts_engine:
            try:
                self.tts_engine.stop()
            except:
                pass
        
        if self.wake_word_detector:
            try:
                self.wake_word_detector.delete()
            except:
                pass
        
        self.logger.info("Voice assistant stopped")

# Factory function
def create_voice_assistant(settings: Settings, logger: Logger) -> VoiceAssistant:
    """Create and configure voice assistant"""
    return VoiceAssistant(settings, logger)

# Voice command utilities
class VoiceCommandProcessor:
    """Helper class for processing voice commands"""
    
    def __init__(self, lewis_core):
        self.lewis_core = lewis_core
    
    async def process_voice_command(self, command: str, user_id: str) -> Dict[str, Any]:
        """Process voice command and return result"""
        
        # Preprocess voice command for better recognition
        processed_command = self._preprocess_voice_command(command)
        
        # Use LEWIS core to process the command
        return await self.lewis_core.process_command(processed_command, user_id)
    
    def _preprocess_voice_command(self, command: str) -> str:
        """Preprocess voice command to handle speech recognition quirks"""
        
        # Common speech recognition corrections
        corrections = {
            "and map": "nmap",
            "n map": "nmap",
            "sequel map": "sqlmap",
            "s q l map": "sqlmap",
            "nikto": "nikto",
            "go buster": "gobuster",
            "metal sploit": "metasploit",
            "metasploit": "metasploit",
            "scan this": "scan",
            "run": "execute",
            "show me": "display",
            "tell me about": "information about"
        }
        
        command_lower = command.lower()
        
        for mistake, correction in corrections.items():
            if mistake in command_lower:
                command = command_lower.replace(mistake, correction)
                break
        
        return command
