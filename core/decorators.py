"""
Decorators for LEWIS Extensions
Provides decorators for registering commands and tools
"""

import functools
from typing import Callable, Any, Optional

def command(name: Optional[str] = None, description: str = ""):
    """
    Decorator to register a function as a LEWIS command
    
    Args:
        name: Command name (uses function name if not provided)
        description: Command description
    """
    def decorator(func: Callable) -> Callable:
        # Set command metadata
        func._lewis_command = True
        func._lewis_command_name = name or func.__name__
        func._lewis_command_description = description
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        # Copy metadata to wrapper
        wrapper._lewis_command = True
        wrapper._lewis_command_name = name or func.__name__
        wrapper._lewis_command_description = description
        
        return wrapper
    return decorator

def tool(name: Optional[str] = None, description: str = ""):
    """
    Decorator to register a function as a LEWIS tool
    
    Args:
        name: Tool name (uses function name if not provided)
        description: Tool description
    """
    def decorator(func: Callable) -> Callable:
        # Set tool metadata
        func._lewis_tool = True
        func._lewis_tool_name = name or func.__name__
        func._lewis_tool_description = description
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        # Copy metadata to wrapper
        wrapper._lewis_tool = True
        wrapper._lewis_tool_name = name or func.__name__
        wrapper._lewis_tool_description = description
        
        return wrapper
    return decorator

def route(path: str, methods: list = None):
    """
    Decorator to register a function as a web route
    
    Args:
        path: URL path
        methods: HTTP methods (default: ['GET'])
    """
    if methods is None:
        methods = ['GET']
        
    def decorator(func: Callable) -> Callable:
        # Set route metadata
        func._lewis_route = True
        func._lewis_route_path = path
        func._lewis_route_methods = methods
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        # Copy metadata to wrapper
        wrapper._lewis_route = True
        wrapper._lewis_route_path = path
        wrapper._lewis_route_methods = methods
        
        return wrapper
    return decorator

def requires_auth(func: Callable) -> Callable:
    """
    Decorator to require authentication for a command/tool
    """
    func._lewis_requires_auth = True
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # In a real implementation, check authentication here
        return func(*args, **kwargs)
    
    wrapper._lewis_requires_auth = True
    return wrapper

def rate_limit(calls_per_minute: int = 60):
    """
    Decorator to apply rate limiting to commands/tools
    
    Args:
        calls_per_minute: Maximum calls allowed per minute
    """
    def decorator(func: Callable) -> Callable:
        func._lewis_rate_limit = calls_per_minute
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # In a real implementation, implement rate limiting here
            return func(*args, **kwargs)
        
        wrapper._lewis_rate_limit = calls_per_minute
        return wrapper
    return decorator

def validate_args(**validators):
    """
    Decorator to validate function arguments
    
    Args:
        **validators: Validation functions for each argument
    """
    def decorator(func: Callable) -> Callable:
        func._lewis_validators = validators
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # In a real implementation, validate arguments here
            return func(*args, **kwargs)
        
        wrapper._lewis_validators = validators
        return wrapper
    return decorator

def cache_result(duration: int = 300):
    """
    Decorator to cache function results
    
    Args:
        duration: Cache duration in seconds
    """
    def decorator(func: Callable) -> Callable:
        func._lewis_cache_duration = duration
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # In a real implementation, implement caching here
            return func(*args, **kwargs)
        
        wrapper._lewis_cache_duration = duration
        return wrapper
    return decorator

def async_task(func: Callable) -> Callable:
    """
    Decorator to mark a function as an async task
    """
    func._lewis_async_task = True
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # In a real implementation, handle async execution here
        return func(*args, **kwargs)
    
    wrapper._lewis_async_task = True
    return wrapper

def log_execution(func: Callable) -> Callable:
    """
    Decorator to log function execution
    """
    func._lewis_log_execution = True
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        import logging
        logger = logging.getLogger(f"lewis.command.{func.__name__}")
        
        logger.info(f"Executing {func.__name__} with args={args}, kwargs={kwargs}")
        try:
            result = func(*args, **kwargs)
            logger.info(f"Successfully executed {func.__name__}")
            return result
        except Exception as e:
            logger.error(f"Error executing {func.__name__}: {e}")
            raise
    
    wrapper._lewis_log_execution = True
    return wrapper
