"""
NLP Processor for LEWIS
Handles natural language processing, intent recognition, and entity extraction
"""

import asyncio
import re
from typing import Dict, Any, List, Tuple
import spacy
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

class NLPProcessor:
    """
    Natural Language Processing engine for LEWIS
    Processes user input to extract intents, entities, and context
    """
    
    def __init__(self, settings, logger):
        self.settings = settings
        self.logger = logger
        
        # Initialize NLP models
        self._initialize_nlp_models()
        
        # Define cybersecurity intent patterns
        self._define_intent_patterns()
        
        # Initialize entity extractors
        self._initialize_entity_extractors()
    
    def _initialize_nlp_models(self):
        """Initialize NLP models and tools"""
        try:
            self.logger.info("🔤 Loading NLP models...")
            
            # Load spaCy model
            model_name = self.settings.get("ai.nlp_model", "en_core_web_sm")
            try:
                self.nlp = spacy.load(model_name)
            except OSError:
                self.logger.warning(f"SpaCy model {model_name} not found, using English model")
                self.nlp = spacy.load("en_core_web_sm")
            
            # Download required NLTK data
            try:
                nltk.data.find('vader_lexicon')
            except LookupError:
                nltk.download('vader_lexicon', quiet=True)
            
            # Initialize sentiment analyzer
            self.sentiment_analyzer = SentimentIntensityAnalyzer()
            
            self.logger.info("✅ NLP models loaded successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to load NLP models: {e}")
            raise
    
    def _define_intent_patterns(self):
        """Define patterns for cybersecurity intent recognition"""
        self.intent_patterns = {
            # Network Scanning
            "network_scanning": [
                r"scan|nmap|port|network|host|ping|discovery",
                r"find.*open.*port|check.*service|enumerate.*service",
                r"reconnaissance|recon|footprint"
            ],
            
            # Vulnerability Assessment
            "vulnerability_assessment": [
                r"vulnerabilit|vuln|cve|security.*issue|weakness",
                r"nikto|openvas|nessus|assess|audit",
                r"web.*scan|application.*scan"
            ],
            
            # Exploitation
            "exploitation": [
                r"exploit|metasploit|payload|shell|backdoor",
                r"attack|penetrat|compromise|gain.*access",
                r"buffer.*overflow|injection|rce"
            ],
            
            # Information Gathering
            "information_gathering": [
                r"subdomain|dns|whois|gather.*info|reconnaissance",
                r"google.*dork|osint|passive.*recon",
                r"social.*engineer|email.*harvest"
            ],
            
            # Report Generation
            "report_generation": [
                r"report|document|summary|findings",
                r"generate.*report|create.*document|export",
                r"pdf|html|executive.*summary"
            ],
            
            # Tool Usage  
            "tool_usage": [
                r"how.*use|tutorial|help.*with|guide",
                r"command|syntax|parameter|option",
                r"example|demo|show.*me"
            ],
            
            # Knowledge Query
            "knowledge_query": [
                r"what.*is|explain|define|tell.*me.*about",
                r"learn.*about|information.*about|details.*about",
                r"how.*does.*work|how.*to"
            ]
        }
    
    def _initialize_entity_extractors(self):
        """Initialize entity extraction patterns"""
        self.entity_patterns = {
            "ip_address": r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b",
            "domain": r"\b[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*\b",
            "url": r"https?://[^\s]+",
            "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "port": r"\bport\s+(\d+)\b",
            "cve": r"CVE-\d{4}-\d{4,7}",
            "file_path": r"[\/\w\.-]+\.[a-zA-Z]{2,4}"
        }
    
    async def process_intent(self, user_input: str) -> Dict[str, Any]:
        """
        Process user input to extract intent, entities, and metadata
        
        Args:
            user_input: Natural language input from user
            
        Returns:
            Dictionary containing processed intent information
        """
        try:
            # Clean and preprocess input
            cleaned_input = self._preprocess_text(user_input)
            
            # Extract intent
            intent, confidence = self._extract_intent(cleaned_input)
            
            # Extract entities
            entities = self._extract_entities(cleaned_input)
            
            # Analyze sentiment
            sentiment = self._analyze_sentiment(cleaned_input)
            
            # Determine if execution is required
            requires_execution = self._requires_execution(intent, entities)
            
            # Generate command suggestions
            command_suggestions = self._generate_command_suggestions(intent, entities)
            
            return {
                "intent": intent,
                "confidence": confidence,
                "entities": entities,
                "sentiment": sentiment,
                "requires_execution": requires_execution,
                "command_suggestions": command_suggestions,
                "processed_text": cleaned_input,
                "original_text": user_input
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error processing intent: {e}")
            return {
                "intent": "unknown",
                "confidence": 0.0,
                "entities": [],
                "error": str(e)
            }
    
    def _preprocess_text(self, text: str) -> str:
        """Clean and preprocess input text"""
        # Convert to lowercase
        text = text.lower().strip()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Handle common abbreviations
        abbreviations = {
            "vulns": "vulnerabilities",
            "recon": "reconnaissance", 
            "enum": "enumeration",
            "creds": "credentials"
        }
        
        for abbrev, full in abbreviations.items():
            text = text.replace(abbrev, full)
        
        return text
    
    def _extract_intent(self, text: str) -> Tuple[str, float]:
        """Extract intent from text using pattern matching"""
        intent_scores = {}
        
        # Score each intent based on pattern matches
        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, text, re.IGNORECASE))
                score += matches
            
            if score > 0:
                intent_scores[intent] = score
        
        # Return highest scoring intent
        if intent_scores:
            best_intent = max(intent_scores, key=intent_scores.get)
            max_score = intent_scores[best_intent]
            confidence = min(max_score / 3.0, 1.0)  # Normalize confidence
            return best_intent, confidence
        
        return "general", 0.1
    
    def _extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """Extract entities from text"""
        entities = []
        
        # Extract using regex patterns
        for entity_type, pattern in self.entity_patterns.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                entities.append({
                    "type": entity_type,
                    "value": match.group().strip(),
                    "start": match.start(),
                    "end": match.end()
                })
        
        # Extract using spaCy NER
        doc = self.nlp(text)
        for ent in doc.ents:
            entities.append({
                "type": ent.label_.lower(),
                "value": ent.text,
                "start": ent.start_char,
                "end": ent.end_char,
                "spacy_type": ent.label_
            })
        
        return entities
    
    def _analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Analyze text sentiment"""
        try:
            # NLTK VADER sentiment
            vader_scores = self.sentiment_analyzer.polarity_scores(text)
            
            # TextBlob sentiment
            blob = TextBlob(text)
            
            return {
                "compound": vader_scores['compound'],
                "positive": vader_scores['pos'],
                "negative": vader_scores['neg'],
                "neutral": vader_scores['neu'],
                "polarity": blob.sentiment.polarity,
                "subjectivity": blob.sentiment.subjectivity
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error analyzing sentiment: {e}")
            return {"compound": 0.0, "positive": 0.0, "negative": 0.0, "neutral": 1.0}
    
    def _requires_execution(self, intent: str, entities: List[Dict]) -> bool:
        """Determine if intent requires command execution"""
        execution_intents = [
            "network_scanning",
            "vulnerability_assessment", 
            "exploitation",
            "information_gathering"
        ]
        
        return intent in execution_intents
    
    def _generate_command_suggestions(
        self, 
        intent: str, 
        entities: List[Dict]
    ) -> List[str]:
        """Generate command suggestions based on intent and entities"""
        suggestions = []
        
        # Extract relevant entity values
        targets = [e['value'] for e in entities if e['type'] in ['ip_address', 'domain', 'url']]
        ports = [e['value'] for e in entities if e['type'] == 'port']
        
        if intent == "network_scanning":
            if targets:
                suggestions.extend([
                    f"nmap -sS {targets[0]}",
                    f"nmap -sV -sC {targets[0]}",
                    f"nmap -p- {targets[0]}"
                ])
            else:
                suggestions.extend([
                    "nmap -sS <target>",
                    "nmap -sV -sC <target>",
                    "masscan -p1-65535 <target>"
                ])
        
        elif intent == "vulnerability_assessment":
            if targets:
                suggestions.extend([
                    f"nikto -h {targets[0]}",
                    f"dirb http://{targets[0]}/",
                    f"gobuster dir -u http://{targets[0]} -w /usr/share/wordlists/common.txt"
                ])
            else:
                suggestions.extend([
                    "nikto -h <target>",
                    "dirb http://<target>/",
                    "sqlmap -u <url> --batch"
                ])
        
        elif intent == "information_gathering":
            if targets:
                suggestions.extend([
                    f"whois {targets[0]}",
                    f"subfinder -d {targets[0]}",
                    f"dig {targets[0]} ANY"
                ])
            else:
                suggestions.extend([
                    "whois <domain>",
                    "subfinder -d <domain>",
                    "theharvester -d <domain> -b google"
                ])
        
        return suggestions
    
    def get_supported_intents(self) -> Dict[str, str]:
        """Get list of supported intents with descriptions"""
        return {
            "network_scanning": "Scan networks, ports, and services",
            "vulnerability_assessment": "Assess vulnerabilities in systems and applications",
            "exploitation": "Exploit identified vulnerabilities (authorized testing only)",
            "information_gathering": "Gather information about targets",
            "report_generation": "Generate security assessment reports",
            "tool_usage": "Get help with cybersecurity tools",
            "knowledge_query": "Query cybersecurity knowledge base"
        }
    
    def is_ready(self) -> bool:
        """Check if NLP processor is ready"""
        return hasattr(self, 'nlp') and hasattr(self, 'sentiment_analyzer')
