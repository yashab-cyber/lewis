"""
AI Engine for LEWIS
Handles natural language understanding, response generation, and AI-driven decisions
"""

import asyncio
import json
from typing import Dict, Any, List, Optional
import torch
from transformers import (
    AutoTokenizer, AutoModelForCausalLM, 
    pipeline, BertTokenizer, BertForSequenceClassification
)
import numpy as np

class AIEngine:
    """
    Core AI engine for LEWIS
    Handles conversation, intent classification, and intelligent responses
    """
    
    def __init__(self, settings, logger, knowledge_base):
        self.settings = settings
        self.logger = logger
        self.knowledge_base = knowledge_base
        
        # Model configurations
        self.model_name = settings.get("ai.model_name", "microsoft/DialoGPT-medium")
        self.max_tokens = settings.get("ai.max_tokens", 512)
        self.temperature = settings.get("ai.temperature", 0.7)
        
        # Initialize models
        self._initialize_models()
        
        # Conversation context
        self.conversation_history = {}
        
        # Cybersecurity-specific intents
        self.cyber_intents = {
            "scan": "network_scanning",
            "vulnerability": "vulnerability_assessment", 
            "exploit": "exploitation",
            "report": "report_generation",
            "learn": "knowledge_query",
            "help": "assistance"
        }
        
    def _initialize_models(self):
        """Initialize AI models"""
        try:
            self.logger.info("🤖 Loading AI models...")
            
            # Device selection
            device = self.settings.get("ai.device", "auto")
            if device == "auto":
                self.device = "cuda" if torch.cuda.is_available() else "cpu"
            else:
                self.device = device
                
            self.logger.info(f"🔧 Using device: {self.device}")
            
            # Load conversational model
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            
            # Add padding token if it doesn't exist
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Intent classification pipeline
            self.intent_classifier = pipeline(
                "text-classification",
                model="microsoft/DialoGPT-medium",
                tokenizer=self.tokenizer,
                device=0 if self.device == "cuda" else -1
            )
            
            # Move models to device
            self.model.to(self.device)
            
            self.logger.info("✅ AI models loaded successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to load AI models: {e}")
            raise
    
    async def generate_response(
        self, 
        user_input: str, 
        intent_result: Dict[str, Any], 
        user_id: str
    ) -> Dict[str, Any]:
        """
        Generate intelligent response based on user input and context
        
        Args:
            user_input: User's natural language input
            intent_result: Processed intent information
            user_id: User identifier
            
        Returns:
            Dictionary containing AI response and metadata
        """
        try:
            # Get conversation context
            context = self._get_conversation_context(user_id)
            
            # Prepare system prompt based on intent
            system_prompt = self._build_system_prompt(intent_result)
            
            # Generate contextual response
            response_text = await self._generate_contextual_response(
                user_input, context, system_prompt
            )
            
            # Add cybersecurity-specific enhancements
            enhanced_response = self._enhance_cyber_response(
                response_text, intent_result
            )
            
            # Update conversation history
            self._update_conversation_history(user_id, user_input, enhanced_response)
            
            return {
                "text": enhanced_response,
                "intent": intent_result.get("intent"),
                "confidence": intent_result.get("confidence", 0.0),
                "suggestions": self._generate_suggestions(intent_result),
                "context_used": len(context) > 0
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error generating AI response: {e}")
            return {
                "text": "I encountered an error processing your request. Please try again.",
                "error": str(e)
            }
    
    def _build_system_prompt(self, intent_result: Dict[str, Any]) -> str:
        """Build system prompt based on detected intent"""
        intent = intent_result.get("intent", "general")
        
        base_prompt = """You are LEWIS, an expert AI cybersecurity assistant. 
You help ethical hackers and security professionals with penetration testing, 
vulnerability assessment, and security analysis. Always prioritize ethical 
hacking practices and legal compliance."""
        
        intent_prompts = {
            "network_scanning": """
Focus on network reconnaissance and scanning techniques. Provide guidance on 
tools like Nmap, masscan, and Zmap. Emphasize proper authorization and scope.""",
            
            "vulnerability_assessment": """
Assist with vulnerability identification and assessment. Reference CVE databases, 
CVSS scores, and remediation strategies. Use tools like Nikto, OpenVAS, and Nessus.""",
            
            "exploitation": """
Provide guidance on exploitation techniques for authorized testing only. 
Reference Metasploit, custom exploits, and post-exploitation techniques. 
Always emphasize legal and ethical boundaries.""",
            
            "report_generation": """
Help create professional security assessment reports. Include executive summaries, 
technical findings, risk ratings, and remediation recommendations.""",
            
            "knowledge_query": """
Answer cybersecurity questions using the latest threat intelligence, 
security best practices, and industry standards."""
        }
        
        specific_prompt = intent_prompts.get(intent, "")
        return f"{base_prompt}\n\n{specific_prompt}"
    
    async def _generate_contextual_response(
        self, 
        user_input: str, 
        context: List[str], 
        system_prompt: str
    ) -> str:
        """Generate response using conversational AI model"""
        try:
            # Prepare input with context
            conversation_text = system_prompt + "\n"
            
            # Add context if available
            if context:
                conversation_text += "Previous context:\n" + "\n".join(context[-3:]) + "\n"
            
            conversation_text += f"User: {user_input}\nLEWIS:"
            
            # Tokenize input
            inputs = self.tokenizer.encode(
                conversation_text, 
                return_tensors="pt", 
                max_length=512, 
                truncation=True
            ).to(self.device)
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=inputs.shape[1] + self.max_tokens,
                    temperature=self.temperature,
                    do_sample=True,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    attention_mask=inputs.ne(self.tokenizer.pad_token_id)
                )
            
            # Decode response
            response = self.tokenizer.decode(
                outputs[0][inputs.shape[1]:], 
                skip_special_tokens=True
            ).strip()
            
            return response or "I need more information to provide a helpful response."
            
        except Exception as e:
            self.logger.error(f"❌ Error in contextual response generation: {e}")
            return "I'm experiencing technical difficulties. Please try rephrasing your question."
    
    def _enhance_cyber_response(
        self, 
        response_text: str, 
        intent_result: Dict[str, Any]
    ) -> str:
        """Add cybersecurity-specific enhancements to response"""
        intent = intent_result.get("intent", "")
        entities = intent_result.get("entities", [])
        
        # Add relevant tool suggestions
        if intent == "network_scanning":
            if "port" in response_text.lower() or "scan" in response_text.lower():
                response_text += "\n\n🔧 Suggested tools: nmap, masscan, zmap"
                
        elif intent == "vulnerability_assessment":
            if "web" in response_text.lower() or "application" in response_text.lower():
                response_text += "\n\n🔧 Suggested tools: nikto, dirb, gobuster, sqlmap"
        
        # Add security warnings
        if any(word in response_text.lower() for word in ["exploit", "attack", "penetrate"]):
            response_text += "\n\n⚠️  Remember: Only perform these actions on systems you own or have explicit authorization to test."
        
        # Add relevant CVE information if available
        if entities:
            cve_info = self.knowledge_base.get_cve_info(entities)
            if cve_info:
                response_text += f"\n\n📊 Related vulnerabilities: {cve_info}"
        
        return response_text
    
    def _generate_suggestions(self, intent_result: Dict[str, Any]) -> List[str]:
        """Generate helpful suggestions based on intent"""
        intent = intent_result.get("intent", "")
        
        suggestions = {
            "network_scanning": [
                "Run a basic port scan",
                "Perform service enumeration", 
                "Check for common vulnerabilities",
                "Generate scan report"
            ],
            "vulnerability_assessment": [
                "Scan web application",
                "Check for SQL injection",
                "Test for XSS vulnerabilities",
                "Review security headers"
            ],
            "exploitation": [
                "Search for exploits",
                "Set up payload",
                "Configure listener",
                "Document findings"
            ],
            "report_generation": [
                "Create executive summary",
                "Add technical findings",
                "Include remediation steps",
                "Export to PDF"
            ]
        }
        
        return suggestions.get(intent, [
            "Ask about cybersecurity tools",
            "Request vulnerability information",
            "Get help with commands",
            "Generate security report"
        ])
    
    def _get_conversation_context(self, user_id: str) -> List[str]:
        """Get conversation context for user"""
        return self.conversation_history.get(user_id, [])
    
    def _update_conversation_history(
        self, 
        user_id: str, 
        user_input: str, 
        response: str
    ):
        """Update conversation history"""
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        self.conversation_history[user_id].extend([
            f"User: {user_input}",
            f"LEWIS: {response}"
        ])
        
        # Keep only last 10 exchanges
        if len(self.conversation_history[user_id]) > 20:
            self.conversation_history[user_id] = self.conversation_history[user_id][-20:]
    
    def is_ready(self) -> bool:
        """Check if AI engine is ready"""
        return hasattr(self, 'model') and hasattr(self, 'tokenizer')
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about loaded models"""
        return {
            "model_name": self.model_name,
            "device": self.device,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "ready": self.is_ready()
        }
