"""
Database Manager for LEWIS
Handles all database operations including user data, logs, and knowledge base
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import json
import hashlib

try:
    from pymongo import MongoClient, IndexModel
    from pymongo.errors import ConnectionFailure, DuplicateKeyError
    MONGODB_AVAILABLE = True
except ImportError:
    MONGODB_AVAILABLE = False

class DatabaseManager:
    """
    Database manager for LEWIS
    Handles MongoDB operations and fallback to file-based storage
    """
    
    def __init__(self, settings, logger):
        self.settings = settings
        self.logger = logger
        
        # Database configuration
        self.mongodb_uri = settings.get("database.mongodb_uri", "mongodb://localhost:27017/")
        self.db_name = settings.get("database.database_name", "lewis_db")
        
        # Collections
        self.collections = {
            "users": settings.get("database.collections.users", "users"),
            "logs": settings.get("database.collections.logs", "execution_logs"),
            "knowledge": settings.get("database.collections.knowledge", "knowledge_base"),
            "reports": settings.get("database.collections.reports", "security_reports")
        }
        
        # Initialize database connection
        self.client = None
        self.db = None
        self.connected = False
        
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize database connection"""
        if not MONGODB_AVAILABLE:
            self.logger.warning("⚠️  MongoDB not available, using file-based storage")
            self._initialize_file_storage()
            return
        
        try:
            self.logger.info("🗄️  Connecting to MongoDB...")
            
            # Create MongoDB client
            self.client = MongoClient(self.mongodb_uri, serverSelectionTimeoutMS=5000)
            
            # Test connection
            self.client.admin.command('ismaster')
            
            # Get database
            self.db = self.client[self.db_name]
            
            # Create indexes
            self._create_indexes()
            
            self.connected = True
            self.logger.info("✅ MongoDB connection established")
            
        except ConnectionFailure as e:
            self.logger.error(f"❌ MongoDB connection failed: {e}")
            self.logger.info("📁 Falling back to file-based storage")
            self._initialize_file_storage()
        except Exception as e:
            self.logger.error(f"❌ Database initialization error: {e}")
            self._initialize_file_storage()
    
    def _initialize_file_storage(self):
        """Initialize file-based storage as fallback"""
        import os
        from pathlib import Path
        
        self.storage_dir = Path("data")
        self.storage_dir.mkdir(exist_ok=True)
        
        # Create storage files
        for collection in self.collections.values():
            storage_file = self.storage_dir / f"{collection}.json"
            if not storage_file.exists():
                storage_file.write_text("[]")
        
        self.connected = True
        self.logger.info("✅ File-based storage initialized")
    
    def _create_indexes(self):
        """Create database indexes for performance"""
        if not self.connected or not self.db:
            return
        
        try:
            # Users collection indexes
            users_collection = self.db[self.collections["users"]]
            users_collection.create_index("user_id", unique=True)
            users_collection.create_index("email", unique=True, sparse=True)
            
            # Logs collection indexes
            logs_collection = self.db[self.collections["logs"]]
            logs_collection.create_index([("timestamp", -1)])
            logs_collection.create_index("user_id")
            logs_collection.create_index("command_type")
            
            # Knowledge collection indexes
            knowledge_collection = self.db[self.collections["knowledge"]]
            knowledge_collection.create_index([("type", 1), ("category", 1)])
            knowledge_collection.create_index("keywords")
            
            # Reports collection indexes
            reports_collection = self.db[self.collections["reports"]]
            reports_collection.create_index([("created_at", -1)])
            reports_collection.create_index("user_id")
            
            self.logger.info("✅ Database indexes created")
            
        except Exception as e:
            self.logger.error(f"❌ Error creating indexes: {e}")
    
    # User Management
    async def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user"""
        try:
            user_data["created_at"] = datetime.utcnow()
            user_data["last_login"] = None
            user_data["active"] = True
            
            # Hash password if provided
            if "password" in user_data:
                user_data["password_hash"] = self._hash_password(user_data.pop("password"))
            
            if self.db:
                result = self.db[self.collections["users"]].insert_one(user_data)
                user_data["_id"] = str(result.inserted_id)
            else:
                # File-based storage
                users = self._load_from_file("users")
                user_data["_id"] = self._generate_id()
                users.append(user_data)
                self._save_to_file("users", users)
            
            self.logger.info(f"✅ User created: {user_data.get('user_id')}")
            return {"success": True, "user": user_data}
            
        except DuplicateKeyError:
            return {"success": False, "error": "User already exists"}
        except Exception as e:
            self.logger.error(f"❌ Error creating user: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        try:
            if self.db:
                user = self.db[self.collections["users"]].find_one({"user_id": user_id})
            else:
                users = self._load_from_file("users")
                user = next((u for u in users if u.get("user_id") == user_id), None)
            
            return user
            
        except Exception as e:
            self.logger.error(f"❌ Error getting user: {e}")
            return None
    
    # Command Logging
    async def log_command(self, log_data: Dict[str, Any]) -> bool:
        """Log command execution"""
        try:
            log_data["timestamp"] = datetime.utcnow()
            log_data["id"] = self._generate_id()
            
            if self.db:
                self.db[self.collections["logs"]].insert_one(log_data)
            else:
                logs = self._load_from_file("logs")
                logs.append(log_data)
                self._save_to_file("logs", logs)
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error logging command: {e}")
            return False
    
    async def get_command_logs(
        self, 
        user_id: str = None, 
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get command execution logs"""
        try:
            if self.db:
                query = {"user_id": user_id} if user_id else {}
                cursor = self.db[self.collections["logs"]].find(query).sort("timestamp", -1).limit(limit)
                return list(cursor)
            else:
                logs = self._load_from_file("logs")
                if user_id:
                    logs = [log for log in logs if log.get("user_id") == user_id]
                return sorted(logs, key=lambda x: x.get("timestamp", ""), reverse=True)[:limit]
            
        except Exception as e:
            self.logger.error(f"❌ Error getting command logs: {e}")
            return []
    
    # Knowledge Base
    async def save_knowledge(self, knowledge_data: Dict[str, Any]) -> bool:
        """Save knowledge base entry"""
        try:
            knowledge_data["created_at"] = datetime.utcnow()
            knowledge_data["id"] = self._generate_id()
            
            if self.db:
                self.db[self.collections["knowledge"]].insert_one(knowledge_data)
            else:
                knowledge = self._load_from_file("knowledge")
                knowledge.append(knowledge_data)
                self._save_to_file("knowledge", knowledge)
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error saving knowledge: {e}")
            return False
    
    async def search_knowledge(
        self, 
        query: str, 
        category: str = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Search knowledge base"""
        try:
            if self.db:
                # MongoDB text search
                search_query = {"$text": {"$search": query}}
                if category:
                    search_query["category"] = category
                
                cursor = self.db[self.collections["knowledge"]].find(search_query).limit(limit)
                return list(cursor)
            else:
                # Simple text search in file storage
                knowledge = self._load_from_file("knowledge")
                results = []
                
                query_lower = query.lower()
                for entry in knowledge:
                    if category and entry.get("category") != category:
                        continue
                    
                    # Search in title and content
                    title = entry.get("title", "").lower()
                    content = entry.get("content", "").lower()
                    
                    if query_lower in title or query_lower in content:
                        results.append(entry)
                    
                    if len(results) >= limit:
                        break
                
                return results
            
        except Exception as e:
            self.logger.error(f"❌ Error searching knowledge: {e}")
            return []
    
    # Reports
    async def save_report(self, report_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save security report"""
        try:
            report_data["created_at"] = datetime.utcnow()
            report_data["id"] = self._generate_id()
            
            if self.db:
                result = self.db[self.collections["reports"]].insert_one(report_data)
                report_data["_id"] = str(result.inserted_id)
            else:
                reports = self._load_from_file("reports")
                reports.append(report_data)
                self._save_to_file("reports", reports)
            
            self.logger.info(f"✅ Report saved: {report_data.get('title')}")
            return {"success": True, "report": report_data}
            
        except Exception as e:
            self.logger.error(f"❌ Error saving report: {e}")
            return {"success": False, "error": str(e)}
    
    async def get_reports(self, user_id: str = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Get security reports"""
        try:
            if self.db:
                query = {"user_id": user_id} if user_id else {}
                cursor = self.db[self.collections["reports"]].find(query).sort("created_at", -1).limit(limit)
                return list(cursor)
            else:
                reports = self._load_from_file("reports")
                if user_id:
                    reports = [r for r in reports if r.get("user_id") == user_id]
                return sorted(reports, key=lambda x: x.get("created_at", ""), reverse=True)[:limit]
            
        except Exception as e:
            self.logger.error(f"❌ Error getting reports: {e}")
            return []
    
    # Utility Methods
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _generate_id(self) -> str:
        """Generate unique ID"""
        return hashlib.md5(f"{datetime.utcnow().isoformat()}".encode()).hexdigest()
    
    def _load_from_file(self, collection: str) -> List[Dict[str, Any]]:
        """Load data from file storage"""
        try:
            storage_file = self.storage_dir / f"{self.collections[collection]}.json"
            if storage_file.exists():
                return json.loads(storage_file.read_text())
            return []
        except Exception as e:
            self.logger.error(f"❌ Error loading from file {collection}: {e}")
            return []
    
    def _save_to_file(self, collection: str, data: List[Dict[str, Any]]):
        """Save data to file storage"""
        try:
            storage_file = self.storage_dir / f"{self.collections[collection]}.json"
            storage_file.write_text(json.dumps(data, indent=2, default=str))
        except Exception as e:
            self.logger.error(f"❌ Error saving to file {collection}: {e}")
    
    # Status and Maintenance
    def is_connected(self) -> bool:
        """Check if database is connected"""
        return self.connected
    
    def get_command_count(self) -> int:
        """Get total command count"""
        try:
            if self.db:
                return self.db[self.collections["logs"]].count_documents({})
            else:
                logs = self._load_from_file("logs")
                return len(logs)
        except Exception:
            return 0
    
    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        try:
            stats = {
                "connected": self.connected,
                "type": "mongodb" if self.db else "file_storage"
            }
            
            if self.db:
                stats.update({
                    "users": self.db[self.collections["users"]].count_documents({}),
                    "logs": self.db[self.collections["logs"]].count_documents({}),
                    "knowledge": self.db[self.collections["knowledge"]].count_documents({}),
                    "reports": self.db[self.collections["reports"]].count_documents({})
                })
            else:
                stats.update({
                    "users": len(self._load_from_file("users")),
                    "logs": len(self._load_from_file("logs")),
                    "knowledge": len(self._load_from_file("knowledge")),
                    "reports": len(self._load_from_file("reports"))
                })
            
            return stats
            
        except Exception as e:
            self.logger.error(f"❌ Error getting database stats: {e}")
            return {"connected": False, "error": str(e)}
    
    def close(self):
        """Close database connection"""
        if self.client:
            self.client.close()
            self.connected = False
            self.logger.info("🗄️  Database connection closed")
