"""
Base Tool Class
===============
Abstract base class for all tools.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import json


class BaseTool(ABC):
    """
    Base class for all agent tools.
    
    Each tool should:
    1. Inherit from this class
    2. Implement the execute() method
    3. Define tool_definition property
    4. Handle errors gracefully
    """
    
    def __init__(self, name: str, description: str):
        """
        Initialize base tool.
        
        Args:
            name: Tool name (used in function calling)
            description: Tool description for LLM
        """
        self.name = name
        self.description = description
    
    @abstractmethod
    def execute(self, **kwargs) -> str:
        """
        Execute the tool with given parameters.
        
        Args:
            **kwargs: Tool-specific parameters
            
        Returns:
            JSON string with results or error
        """
        pass
    
    @property
    @abstractmethod
    def tool_definition(self) -> Dict[str, Any]:
        """
        Return OpenAI function calling format definition.
        
        Returns:
            Tool definition dictionary
        """
        pass
    
    def format_error(self, error: Exception, **context) -> str:
        """
        Format error message as JSON.
        
        Args:
            error: Exception that occurred
            **context: Additional context
            
        Returns:
            JSON string with error details
        """
        return json.dumps({
            "error": str(error),
            "tool": self.name,
            **context
        }, indent=2)
    
    def format_success(self, data: Any, **metadata) -> str:
        """
        Format success response as JSON.
        
        Args:
            data: Response data
            **metadata: Additional metadata
            
        Returns:
            JSON string with results
        """
        return json.dumps({
            "success": True,
            "data": data,
            "tool": self.name,
            **metadata
        }, indent=2)
    
    def __call__(self, **kwargs) -> str:
        """
        Allow tool to be called as a function.
        
        Args:
            **kwargs: Tool parameters
            
        Returns:
            Tool execution result
        """
        return self.execute(**kwargs)
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(name='{self.name}')>"
