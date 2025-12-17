"""
Configuration
============
Environment and settings management.
"""

import os
import yaml
from typing import Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """
    Configuration manager for the agent system.
    
    Handles:
    - Environment variables
    - Default settings
    - Model configurations
    - API keys
    """
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration.
        
        Args:
            config_file: Path to YAML config file (optional)
        """
        self.config_file = config_file
        self.settings: Dict[str, Any] = {}
        
        # Load from file if provided
        if config_file and os.path.exists(config_file):
            with open(config_file, 'r') as f:
                self.settings = yaml.safe_load(f) or {}
        
        # Initialize default settings
        self._init_defaults()
    
    def _init_defaults(self):
        """Initialize default configuration values."""
        defaults = {
            # API Keys
            "openai_api_key": os.getenv("OPENAI_API_KEY"),
            "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY"),
            "tavily_api_key": os.getenv("TAVILY_API_KEY"),
            
            # Model Settings
            "default_model": "gpt-4-turbo-preview",
            "temperature": 0.0,
            "max_tokens": None,
            
            # Agent Settings
            "max_tool_turns": 5,
            "enable_tools": True,
            
            # Research Settings
            "max_search_results": 10,
            "max_arxiv_results": 5,
            
            # Output Settings
            "output_dir": "./outputs",
            "save_format": "markdown",
            
            # Debug Settings
            "verbose": False,
            "debug": False
        }
        
        # Merge with loaded settings (loaded settings take precedence)
        for key, value in defaults.items():
            if key not in self.settings:
                self.settings[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any):
        """
        Set configuration value.
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self.settings[key] = value
    
    def validate_api_keys(self) -> Dict[str, bool]:
        """
        Validate API keys.
        
        Returns:
            Dict with validation results for each provider
        """
        return {
            "openai": bool(self.get("openai_api_key")),
            "anthropic": bool(self.get("anthropic_api_key")),
            "tavily": bool(self.get("tavily_api_key"))
        }
    
    def get_model_config(self, model: Optional[str] = None) -> Dict[str, Any]:
        """
        Get model configuration.
        
        Args:
            model: Model name (uses default if not provided)
            
        Returns:
            Dict with model settings
        """
        model = model or self.get("default_model")
        
        return {
            "model": model,
            "temperature": self.get("temperature"),
            "max_tokens": self.get("max_tokens")
        }
    
    def save(self, path: Optional[str] = None):
        """
        Save configuration to YAML file.
        
        Args:
            path: Output path (uses config_file if not provided)
        """
        path = path or self.config_file
        if not path:
            raise ValueError("No path specified for saving config")
        
        with open(path, 'w') as f:
            yaml.dump(self.settings, f, default_flow_style=False)
    
    def __repr__(self):
        """String representation."""
        masked_settings = self.settings.copy()
        
        # Mask API keys
        for key in ["openai_api_key", "anthropic_api_key", "tavily_api_key"]:
            if masked_settings.get(key):
                masked_settings[key] = "***masked***"
        
        return f"Config({masked_settings})"


# Global config instance
_global_config = None


def load_config(config_file: Optional[str] = None) -> Config:
    """
    Load or get global configuration.
    
    Args:
        config_file: Path to YAML config file (optional)
        
    Returns:
        Config instance
    """
    global _global_config
    if _global_config is None:
        _global_config = Config(config_file)
    return _global_config


def get_config() -> Config:
    """
    Get global configuration instance.
    
    Returns:
        Config instance
    """
    return load_config()


def create_example_config(path: str = "config.example.yaml"):
    """
    Create example configuration file.
    
    Args:
        path: Output path for example config
    """
    example = {
        "# API Keys": None,
        "openai_api_key": "sk-...",
        "anthropic_api_key": "sk-ant-...",
        "tavily_api_key": "tvly-...",
        
        "# Model Settings": None,
        "default_model": "gpt-4-turbo-preview",
        "temperature": 0.0,
        "max_tokens": None,
        
        "# Agent Settings": None,
        "max_tool_turns": 5,
        "enable_tools": True,
        
        "# Research Settings": None,
        "max_search_results": 10,
        "max_arxiv_results": 5,
        
        "# Output Settings": None,
        "output_dir": "./outputs",
        "save_format": "markdown",
        
        "# Debug Settings": None,
        "verbose": False,
        "debug": False
    }
    
    with open(path, 'w') as f:
        yaml.dump(example, f, default_flow_style=False)
    
    print(f"Example config created at: {path}")
