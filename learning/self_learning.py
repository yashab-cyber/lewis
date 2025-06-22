"""
Self-Learning Engine for LEWIS
Implements machine learning-based adaptation and continuous learning
"""

import asyncio
import json
import pickle
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
import threading
import time

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.pipeline import Pipeline
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

class SelfLearningEngine:
    """
    Self-learning engine for LEWIS
    Learns from user interactions and improves responses over time
    """
    
    def __init__(self, settings, logger, knowledge_base, ai_engine):
        self.settings = settings
        self.logger = logger
        self.knowledge_base = knowledge_base
        self.ai_engine = ai_engine
        
        # Learning configuration
        self.learning_enabled = settings.get("learning.enabled", True)
        self.update_interval = settings.get("learning.update_interval", 3600)
        self.max_examples = settings.get("learning.max_learning_examples", 10000)
        
        # Learning models
        self.intent_classifier = None
        self.command_success_predictor = None
        self.response_quality_scorer = None
        
        # Training data
        self.training_data = {
            "intents": [],
            "commands": [],
            "responses": []
        }
        
        # Learning state
        self.learning_active = False
        self.last_model_update = None
        self.learning_thread = None
        
        # Performance metrics
        self.metrics = {
            "interactions_learned": 0,
            "model_accuracy": 0.0,
            "last_training_time": None,
            "successful_predictions": 0,
            "total_predictions": 0
        }
        
        # Initialize learning engine
        self._initialize_learning_engine()
    
    def _initialize_learning_engine(self):
        """Initialize the learning engine"""
        try:
            if not SKLEARN_AVAILABLE:
                self.logger.warning("⚠️  Scikit-learn not available, learning features disabled")
                self.learning_enabled = False
                return
            
            if not self.learning_enabled:
                self.logger.info("🧠 Learning engine disabled in configuration")
                return
            
            self.logger.info("🧠 Initializing self-learning engine...")
            
            # Load existing models if available
            self._load_existing_models()
            
            # Load training data
            self._load_training_data()
            
            # Initialize models if not loaded
            if not self.intent_classifier:
                self._initialize_models()
            
            self.logger.info("✅ Self-learning engine initialized")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize learning engine: {e}")
            self.learning_enabled = False
    
    def _initialize_models(self):
        """Initialize machine learning models"""
        try:
            # Intent classification model
            self.intent_classifier = Pipeline([
                ('tfidf', TfidfVectorizer(max_features=1000, stop_words='english')),
                ('classifier', MultinomialNB())
            ])
            
            # Command success prediction model
            self.command_success_predictor = Pipeline([
                ('tfidf', TfidfVectorizer(max_features=500)),
                ('classifier', MultinomialNB())
            ])
            
            self.logger.info("✅ ML models initialized")
            
        except Exception as e:
            self.logger.error(f"❌ Error initializing models: {e}")
    
    async def learn_from_interaction(
        self,
        user_input: str,
        intent_result: Dict[str, Any],
        ai_response: Dict[str, Any],
        execution_result: Optional[Dict[str, Any]] = None
    ):
        """
        Learn from user interaction
        
        Args:
            user_input: Original user input
            intent_result: Processed intent information
            ai_response: AI response generated
            execution_result: Command execution result if any
        """
        try:
            if not self.learning_enabled:
                return
            
            # Create learning example
            learning_example = {
                "timestamp": datetime.utcnow().isoformat(),
                "user_input": user_input,
                "intent": intent_result.get("intent"),
                "confidence": intent_result.get("confidence", 0.0),
                "entities": intent_result.get("entities", []),
                "ai_response": ai_response.get("text", ""),
                "response_quality": self._assess_response_quality(ai_response),
                "execution_success": execution_result.get("success") if execution_result else None,
                "execution_time": execution_result.get("execution_time") if execution_result else None
            }
            
            # Add to training data
            self._add_training_example(learning_example)
            
            # Update metrics
            self.metrics["interactions_learned"] += 1
            
            # Trigger model update if needed
            if self._should_update_models():
                asyncio.create_task(self._update_models())
            
            self.logger.debug(f"🧠 Learned from interaction: {user_input[:50]}...")
            
        except Exception as e:
            self.logger.error(f"❌ Error learning from interaction: {e}")
    
    def _assess_response_quality(self, ai_response: Dict[str, Any]) -> float:
        """Assess quality of AI response"""
        try:
            score = 0.0
            
            # Basic quality indicators
            response_text = ai_response.get("text", "")
            
            # Length check (not too short, not too long)
            if 20 <= len(response_text) <= 500:
                score += 0.3
            
            # Confidence score
            confidence = ai_response.get("confidence", 0.0)
            score += confidence * 0.3
            
            # Presence of suggestions
            if ai_response.get("suggestions"):
                score += 0.2
            
            # Context usage
            if ai_response.get("context_used"):
                score += 0.2
            
            return min(score, 1.0)
            
        except Exception as e:
            self.logger.error(f"❌ Error assessing response quality: {e}")
            return 0.5
    
    def _add_training_example(self, example: Dict[str, Any]):
        """Add example to training data"""
        try:
            # Add to intent training data
            self.training_data["intents"].append({
                "text": example["user_input"],
                "intent": example["intent"],
                "confidence": example["confidence"]
            })
            
            # Add to command success data
            if example["execution_success"] is not None:
                self.training_data["commands"].append({
                    "text": example["user_input"],
                    "success": example["execution_success"],
                    "execution_time": example["execution_time"]
                })
            
            # Add to response quality data
            self.training_data["responses"].append({
                "text": example["user_input"],
                "response": example["ai_response"],
                "quality": example["response_quality"]
            })
            
            # Limit training data size
            for data_type in self.training_data:
                if len(self.training_data[data_type]) > self.max_examples:
                    # Remove oldest examples
                    self.training_data[data_type] = self.training_data[data_type][-self.max_examples:]
            
        except Exception as e:
            self.logger.error(f"❌ Error adding training example: {e}")
    
    def _should_update_models(self) -> bool:
        """Check if models should be updated"""
        if not self.last_model_update:
            return len(self.training_data["intents"]) >= 50
        
        # Check time since last update
        time_diff = datetime.utcnow() - self.last_model_update
        if time_diff.total_seconds() > self.update_interval:
            return True
        
        # Check if enough new data
        interactions_since_update = self.metrics["interactions_learned"]
        return interactions_since_update >= 100
    
    async def _update_models(self):
        """Update machine learning models with new data"""
        try:
            self.logger.info("🔄 Updating learning models...")
            
            # Update intent classifier
            if len(self.training_data["intents"]) >= 20:
                await self._update_intent_classifier()
            
            # Update command success predictor
            if len(self.training_data["commands"]) >= 20:
                await self._update_command_predictor()
            
            # Save updated models
            self._save_models()
            
            # Update metrics
            self.last_model_update = datetime.utcnow()
            self.metrics["last_training_time"] = self.last_model_update.isoformat()
            
            self.logger.info("✅ Learning models updated successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Error updating models: {e}")
    
    async def _update_intent_classifier(self):
        """Update intent classification model"""
        try:
            intent_data = self.training_data["intents"]
            
            # Prepare training data
            texts = [item["text"] for item in intent_data]
            intents = [item["intent"] for item in intent_data]
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                texts, intents, test_size=0.2, random_state=42
            )
            
            # Train model
            self.intent_classifier.fit(X_train, y_train)
            
            # Evaluate
            y_pred = self.intent_classifier.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            self.metrics["model_accuracy"] = accuracy
            self.logger.info(f"📊 Intent classifier accuracy: {accuracy:.3f}")
            
        except Exception as e:
            self.logger.error(f"❌ Error updating intent classifier: {e}")
    
    async def _update_command_predictor(self):
        """Update command success prediction model"""
        try:
            command_data = self.training_data["commands"]
            
            # Prepare training data
            texts = [item["text"] for item in command_data]
            success_labels = [item["success"] for item in command_data]
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                texts, success_labels, test_size=0.2, random_state=42
            )
            
            # Train model
            self.command_success_predictor.fit(X_train, y_train)
            
            # Evaluate
            y_pred = self.command_success_predictor.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            self.logger.info(f"📊 Command predictor accuracy: {accuracy:.3f}")
            
        except Exception as e:
            self.logger.error(f"❌ Error updating command predictor: {e}")
    
    def predict_intent(self, user_input: str) -> Tuple[str, float]:
        """Predict intent using learned model"""
        try:
            if not self.intent_classifier or not self.learning_enabled:
                return "unknown", 0.0
            
            # Predict intent
            predicted_intent = self.intent_classifier.predict([user_input])[0]
            
            # Get confidence (simplified)
            probabilities = self.intent_classifier.predict_proba([user_input])[0]
            confidence = np.max(probabilities)
            
            # Update prediction metrics
            self.metrics["total_predictions"] += 1
            
            return predicted_intent, confidence
            
        except Exception as e:
            self.logger.error(f"❌ Error predicting intent: {e}")
            return "unknown", 0.0
    
    def predict_command_success(self, command: str) -> float:
        """Predict likelihood of command success"""
        try:
            if not self.command_success_predictor or not self.learning_enabled:
                return 0.5
            
            # Predict success probability
            probabilities = self.command_success_predictor.predict_proba([command])[0]
            success_probability = probabilities[1] if len(probabilities) > 1 else 0.5
            
            return success_probability
            
        except Exception as e:
            self.logger.error(f"❌ Error predicting command success: {e}")
            return 0.5
    
    def start_background_learning(self):
        """Start background learning process"""
        if not self.learning_enabled:
            return
        
        self.learning_active = True
        self.learning_thread = threading.Thread(target=self._background_learning_loop, daemon=True)
        self.learning_thread.start()
        
        self.logger.info("🧠 Background learning started")
    
    def _background_learning_loop(self):
        """Background learning loop"""
        while self.learning_active:
            try:
                # Sleep for update interval
                time.sleep(self.update_interval)
                
                # Update knowledge base
                asyncio.run(self.knowledge_base.update_cve_data())
                
                # Perform model maintenance
                self._perform_model_maintenance()
                
            except Exception as e:
                self.logger.error(f"❌ Error in background learning: {e}")
    
    def _perform_model_maintenance(self):
        """Perform model maintenance tasks"""
        try:
            # Clean old training data
            self._clean_old_training_data()
            
            # Update model performance metrics
            self._update_performance_metrics()
            
        except Exception as e:
            self.logger.error(f"❌ Error in model maintenance: {e}")
    
    def _clean_old_training_data(self):
        """Remove old training data to prevent memory issues"""
        cutoff_date = datetime.utcnow() - timedelta(days=30)
        
        for data_type in self.training_data:
            original_count = len(self.training_data[data_type])
            
            # Keep only recent data (if timestamps available)
            # Simplified implementation - in real version, check timestamps
            if original_count > self.max_examples:
                self.training_data[data_type] = self.training_data[data_type][-self.max_examples:]
                
                removed_count = original_count - len(self.training_data[data_type])
                if removed_count > 0:
                    self.logger.debug(f"🧹 Cleaned {removed_count} old {data_type} examples")
    
    def _update_performance_metrics(self):
        """Update learning performance metrics"""
        try:
            # Calculate success rate
            if self.metrics["total_predictions"] > 0:
                success_rate = self.metrics["successful_predictions"] / self.metrics["total_predictions"]
                self.metrics["prediction_success_rate"] = success_rate
            
            # Log metrics periodically
            if self.metrics["interactions_learned"] % 100 == 0:
                self.logger.info(f"📊 Learning metrics: {self.metrics}")
                
        except Exception as e:
            self.logger.error(f"❌ Error updating performance metrics: {e}")
    
    def _save_models(self):
        """Save trained models to disk"""
        try:
            models_dir = Path("models")
            models_dir.mkdir(exist_ok=True)
            
            # Save intent classifier
            if self.intent_classifier:
                with open(models_dir / "intent_classifier.pkl", "wb") as f:
                    pickle.dump(self.intent_classifier, f)
            
            # Save command predictor
            if self.command_success_predictor:
                with open(models_dir / "command_predictor.pkl", "wb") as f:
                    pickle.dump(self.command_success_predictor, f)
            
            # Save training data
            with open(models_dir / "training_data.json", "w") as f:
                json.dump(self.training_data, f, indent=2)
            
            # Save metrics
            with open(models_dir / "metrics.json", "w") as f:
                json.dump(self.metrics, f, indent=2)
                
            self.logger.debug("💾 Models saved to disk")
            
        except Exception as e:
            self.logger.error(f"❌ Error saving models: {e}")
    
    def _load_existing_models(self):
        """Load existing models from disk"""
        try:
            models_dir = Path("models")
            
            if not models_dir.exists():
                return
            
            # Load intent classifier
            intent_file = models_dir / "intent_classifier.pkl"
            if intent_file.exists():
                with open(intent_file, "rb") as f:
                    self.intent_classifier = pickle.load(f)
                    self.logger.info("📂 Intent classifier loaded")
            
            # Load command predictor
            predictor_file = models_dir / "command_predictor.pkl"
            if predictor_file.exists():
                with open(predictor_file, "rb") as f:
                    self.command_success_predictor = pickle.load(f)
                    self.logger.info("📂 Command predictor loaded")
            
            # Load metrics
            metrics_file = models_dir / "metrics.json"
            if metrics_file.exists():
                with open(metrics_file, "r") as f:
                    saved_metrics = json.load(f)
                    self.metrics.update(saved_metrics)
                    self.logger.info("📊 Metrics loaded")
                    
        except Exception as e:
            self.logger.error(f"❌ Error loading existing models: {e}")
    
    def _load_training_data(self):
        """Load existing training data"""
        try:
            models_dir = Path("models")
            training_file = models_dir / "training_data.json"
            
            if training_file.exists():
                with open(training_file, "r") as f:
                    self.training_data = json.load(f)
                    self.logger.info("📂 Training data loaded")
                    
        except Exception as e:
            self.logger.error(f"❌ Error loading training data: {e}")
    
    def stop(self):
        """Stop learning engine"""
        self.learning_active = False
        
        if self.learning_thread and self.learning_thread.is_alive():
            self.learning_thread.join(timeout=5)
        
        # Save models before stopping
        self._save_models()
        
        self.logger.info("🧠 Learning engine stopped")
    
    def is_active(self) -> bool:
        """Check if learning engine is active"""
        return self.learning_enabled and self.learning_active
    
    def get_learning_stats(self) -> Dict[str, Any]:
        """Get learning statistics"""
        return {
            "enabled": self.learning_enabled,
            "active": self.learning_active,
            "interactions_learned": self.metrics["interactions_learned"],
            "model_accuracy": self.metrics.get("model_accuracy", 0.0),
            "training_data_size": {
                "intents": len(self.training_data["intents"]),
                "commands": len(self.training_data["commands"]),
                "responses": len(self.training_data["responses"])
            },
            "last_update": self.metrics.get("last_training_time")
        }
