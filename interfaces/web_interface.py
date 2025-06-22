#!/usr/bin/env python3
"""
LEWIS Web Interface
Provides REST API and web dashboard for LEWIS system
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import uvicorn

from core.lewis_core import LewisCore
from config.settings import Settings
from utils.logger import Logger
from security.security_manager import SecurityManager

class CommandRequest(BaseModel):
    input: str
    user_id: str
    session_id: Optional[str] = None

class ReportRequest(BaseModel):
    type: str = "vulnerability"
    format: str = "pdf"
    filters: Optional[Dict[str, Any]] = None

class WebInterface:
    """Web interface for LEWIS with REST API and dashboard"""
    
    def __init__(self, lewis_core: LewisCore, settings: Settings, logger: Logger):
        self.lewis_core = lewis_core
        self.settings = settings
        self.logger = logger
        self.security_manager = SecurityManager(settings, logger)
        
        # Initialize FastAPI app
        self.app = FastAPI(
            title="LEWIS API",
            description="Linux Environment Working Intelligence System API",
            version="1.0.0",
            docs_url="/api/docs",
            redoc_url="/api/redoc"
        )
        
        # Add CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Setup templates and static files
        self.templates = Jinja2Templates(directory="interfaces/templates")
        
        # WebSocket connections
        self.active_connections: Dict[str, WebSocket] = {}
        
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup API routes"""
        
        # Authentication dependency
        security = HTTPBearer()
        
        async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
            try:
                user = self.security_manager.verify_token(credentials.credentials)
                if not user:
                    raise HTTPException(status_code=401, detail="Invalid token")
                return user
            except Exception as e:
                raise HTTPException(status_code=401, detail="Authentication failed")
        
        # Health check
        @self.app.get("/api/health")
        async def health_check():
            return {"status": "healthy", "timestamp": datetime.now().isoformat()}
        
        # System status
        @self.app.get("/api/status")
        async def get_status(user: dict = Depends(get_current_user)):
            try:
                status = await self.lewis_core.get_system_status()
                return {"status": "success", "data": status}
            except Exception as e:
                self.logger.error(f"Error getting system status: {str(e)}")
                raise HTTPException(status_code=500, detail="Failed to get system status")
        
        # Process command
        @self.app.post("/api/command")
        async def process_command(request: CommandRequest, user: dict = Depends(get_current_user)):
            try:
                # Validate user permissions
                if not self.security_manager.check_permissions(user.get("user_id"), "execute_commands"):
                    raise HTTPException(status_code=403, detail="Insufficient permissions")
                
                result = await self.lewis_core.process_command(
                    request.input, 
                    request.user_id,
                    session_id=request.session_id
                )
                
                return {"status": "success", "data": result}
            except Exception as e:
                self.logger.error(f"Error processing command: {str(e)}")
                raise HTTPException(status_code=500, detail="Command processing failed")
        
        # Generate report
        @self.app.post("/api/report")
        async def generate_report(request: ReportRequest, user: dict = Depends(get_current_user)):
            try:
                # Import report generator
                from reports.report_generator import ReportGenerator
                
                report_gen = ReportGenerator(self.settings, self.logger)
                report_path = await report_gen.generate_report(
                    report_type=request.type,
                    format=request.format,
                    filters=request.filters,
                    user_id=user.get("user_id")
                )
                
                return {"status": "success", "report_path": str(report_path)}
            except Exception as e:
                self.logger.error(f"Error generating report: {str(e)}")
                raise HTTPException(status_code=500, detail="Report generation failed")
        
        # Get available tools
        @self.app.get("/api/tools")
        async def get_tools(user: dict = Depends(get_current_user)):
            try:
                tools = await self.lewis_core.tool_manager.get_available_tools()
                return {"status": "success", "data": tools}
            except Exception as e:
                self.logger.error(f"Error getting tools: {str(e)}")
                raise HTTPException(status_code=500, detail="Failed to get tools")
        
        # Analytics data
        @self.app.get("/api/analytics")
        async def get_analytics(user: dict = Depends(get_current_user)):
            try:
                from analytics.analytics_engine import AnalyticsEngine
                
                analytics = AnalyticsEngine(self.settings, self.logger)
                data = await analytics.get_dashboard_data(user.get("user_id"))
                
                return {"status": "success", "data": data}
            except Exception as e:
                self.logger.error(f"Error getting analytics: {str(e)}")
                raise HTTPException(status_code=500, detail="Failed to get analytics")
        
        # WebSocket endpoint for real-time communication
        @self.app.websocket("/ws/{client_id}")
        async def websocket_endpoint(websocket: WebSocket, client_id: str):
            await websocket.accept()
            self.active_connections[client_id] = websocket
            
            try:
                while True:
                    data = await websocket.receive_text()
                    message = json.loads(data)
                    
                    # Process WebSocket message
                    response = await self._process_websocket_message(message, client_id)
                    await websocket.send_text(json.dumps(response))
                    
            except WebSocketDisconnect:
                if client_id in self.active_connections:
                    del self.active_connections[client_id]
          # Serve dashboard
        @self.app.get("/", response_class=HTMLResponse)
        async def dashboard():
            return self.templates.TemplateResponse("dashboard.html", {"request": {}})
        
        # Serve extensions dashboard
        @self.app.get("/extensions", response_class=HTMLResponse)
        async def extensions_dashboard():
            return self.templates.TemplateResponse("extensions.html", {"request": {}})
        
        # Serve static files
        self.app.mount("/static", StaticFiles(directory="interfaces/static"), name="static")
    
        # Get extensions
        @self.app.get("/api/extensions")
        async def get_extensions(user: dict = Depends(get_current_user)):
            try:
                extension_status = self.lewis_core.get_extension_status()
                return {"status": "success", "data": extension_status}
            except Exception as e:
                self.logger.error(f"Error getting extensions: {str(e)}")
                raise HTTPException(status_code=500, detail="Failed to get extensions")
        
        # Reload extensions
        @self.app.post("/api/extensions/reload")
        async def reload_extensions(user: dict = Depends(get_current_user)):
            try:
                # Check admin permissions
                if not self.security_manager.check_permissions(user.get("user_id"), "manage_extensions"):
                    raise HTTPException(status_code=403, detail="Admin permissions required")
                
                # Reload extensions
                self.lewis_core.extension_manager.unload_all_extensions()
                self.lewis_core.extension_manager.load_all_extensions()
                
                # Get updated status
                extension_status = self.lewis_core.get_extension_status()
                
                return {
                    "status": "success", 
                    "message": "Extensions reloaded successfully",
                    "data": extension_status
                }
            except Exception as e:
                self.logger.error(f"Error reloading extensions: {str(e)}")
                raise HTTPException(status_code=500, detail="Failed to reload extensions")
        
        # Get extension commands
        @self.app.get("/api/extensions/commands")
        async def get_extension_commands(user: dict = Depends(get_current_user)):
            try:
                available_commands = self.lewis_core.get_available_commands()
                extension_commands = {}
                
                # Filter extension commands
                extension_status = self.lewis_core.get_extension_status()
                if extension_status and extension_status.get("loaded_extensions"):
                    for ext_name, ext_info in extension_status["loaded_extensions"].items():
                        ext_commands = ext_info.get("commands", [])
                        for cmd in ext_commands:
                            if cmd in available_commands:
                                extension_commands[cmd] = {
                                    "description": available_commands[cmd],
                                    "extension": ext_name
                                }
                
                return {"status": "success", "data": extension_commands}
            except Exception as e:
                self.logger.error(f"Error getting extension commands: {str(e)}")
                raise HTTPException(status_code=500, detail="Failed to get extension commands")

        # ...existing code...
    
    async def _process_websocket_message(self, message: Dict[str, Any], client_id: str) -> Dict[str, Any]:
        """Process WebSocket message"""
        try:
            msg_type = message.get("type")
            
            if msg_type == "command":
                result = await self.lewis_core.process_command(
                    message.get("input", ""),
                    message.get("user_id", client_id)
                )
                return {"type": "command_result", "data": result}
            
            elif msg_type == "status":
                status = await self.lewis_core.get_system_status()
                return {"type": "status_update", "data": status}
            
            else:
                return {"type": "error", "message": "Unknown message type"}
                
        except Exception as e:
            self.logger.error(f"WebSocket message processing error: {str(e)}")
            return {"type": "error", "message": "Message processing failed"}
    
    async def broadcast_message(self, message: Dict[str, Any]):
        """Broadcast message to all connected clients"""
        if self.active_connections:
            disconnected = []
            for client_id, websocket in self.active_connections.items():
                try:
                    await websocket.send_text(json.dumps(message))
                except:
                    disconnected.append(client_id)
            
            # Clean up disconnected clients
            for client_id in disconnected:
                del self.active_connections[client_id]
    
    def run(self, host: str = "0.0.0.0", port: int = 8000, debug: bool = False):
        """Run the web server"""
        self.logger.info(f"Starting LEWIS web interface on {host}:{port}")
        
        uvicorn.run(
            self.app,
            host=host,
            port=port,
            debug=debug,
            log_level="info" if not debug else "debug"
        )

# Factory function for creating web interface
def create_web_interface(lewis_core: LewisCore, settings: Settings, logger: Logger) -> WebInterface:
    """Create and configure web interface"""
    return WebInterface(lewis_core, settings, logger)

if __name__ == "__main__":
    # This allows running the web interface standalone
    import sys
    sys.path.append("..")
    
    from config.settings import load_settings
    from utils.logger import setup_logger
    
    settings = load_settings()
    logger = setup_logger(settings)
    
    # Mock lewis_core for standalone testing
    class MockLewisCore:
        async def process_command(self, command, user_id, session_id=None):
            return {"output": f"Mock response for: {command}", "success": True}
        
        async def get_system_status(self):
            return {"status": "running", "uptime": "1h 23m", "memory_usage": "45%"}
    
    mock_core = MockLewisCore()
    web_interface = create_web_interface(mock_core, settings, logger)
    web_interface.run(debug=True)
