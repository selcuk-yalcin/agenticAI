"""
LLM Client
==========
Unified client for OpenAI and Anthropic LLMs with function calling support.
"""

import os
import json
from typing import List, Dict, Any, Optional, Tuple
from dotenv import load_dotenv
from openai import OpenAI
from anthropic import Anthropic

# Load environment variables
load_dotenv()


class LLMClient:
    """
    Unified LLM client supporting OpenAI and Anthropic models.
    
    Features:
    - Automatic provider detection from model name
    - Function calling support
    - Tool execution loop
    - Error handling
    """
    
    def __init__(
        self,
        openai_api_key: Optional[str] = None,
        anthropic_api_key: Optional[str] = None
    ):
        """
        Initialize LLM client.
        
        Args:
            openai_api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            anthropic_api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
        """
        # Initialize OpenAI
        self.openai_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if self.openai_key:
            self.openai_client = OpenAI(api_key=self.openai_key)
        else:
            self.openai_client = None
        
        # Initialize Anthropic
        self.anthropic_key = anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")
        if self.anthropic_key:
            self.anthropic_client = Anthropic(api_key=self.anthropic_key)
        else:
            self.anthropic_client = None
    
    def is_anthropic_model(self, model: str) -> bool:
        """Check if model is from Anthropic."""
        return "claude" in model.lower() or "anthropic" in model.lower()
    
    def is_openai_model(self, model: str) -> bool:
        """Check if model is from OpenAI."""
        return "gpt" in model.lower() or "o1" in model.lower() or "o3" in model.lower()
    
    def chat_completion(
        self,
        model: str,
        messages: List[Dict[str, Any]],
        temperature: float = 0.0,
        max_tokens: Optional[int] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: str = "auto"
    ) -> Any:
        """
        Create chat completion with automatic provider selection.
        
        Args:
            model: Model name (e.g., "gpt-4-turbo-preview", "claude-3-opus")
            messages: List of message dictionaries
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate
            tools: Tool definitions for function calling
            tool_choice: How to choose tools ("auto", "none", or specific)
            
        Returns:
            Response object from the provider
        """
        if self.is_anthropic_model(model):
            return self._anthropic_completion(
                model, messages, temperature, max_tokens
            )
        elif self.is_openai_model(model):
            return self._openai_completion(
                model, messages, temperature, max_tokens, tools, tool_choice
            )
        else:
            raise ValueError(f"Unknown model provider for: {model}")
    
    def _openai_completion(
        self,
        model: str,
        messages: List[Dict[str, Any]],
        temperature: float,
        max_tokens: Optional[int],
        tools: Optional[List[Dict[str, Any]]],
        tool_choice: str
    ) -> Any:
        """OpenAI completion."""
        if not self.openai_client:
            raise ValueError("OpenAI API key not configured")
        
        kwargs = {
            "model": model,
            "messages": messages,
            "temperature": temperature
        }
        
        if max_tokens:
            kwargs["max_tokens"] = max_tokens
        
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = tool_choice
        
        return self.openai_client.chat.completions.create(**kwargs)
    
    def _anthropic_completion(
        self,
        model: str,
        messages: List[Dict[str, Any]],
        temperature: float,
        max_tokens: Optional[int]
    ) -> Any:
        """Anthropic completion."""
        if not self.anthropic_client:
            raise ValueError("Anthropic API key not configured")
        
        # Convert OpenAI format to Anthropic format
        system_message = None
        anthropic_messages = []
        
        for msg in messages:
            if msg["role"] == "system":
                system_message = msg["content"]
            else:
                anthropic_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        
        kwargs = {
            "model": model,
            "messages": anthropic_messages,
            "temperature": temperature,
            "max_tokens": max_tokens or 4096
        }
        
        if system_message:
            kwargs["system"] = system_message
        
        return self.anthropic_client.messages.create(**kwargs)
    
    def execute_tool_loop(
        self,
        model: str,
        messages: List[Dict[str, Any]],
        tools: List[Dict[str, Any]],
        tool_functions: Dict[str, callable],
        max_turns: int = 5,
        temperature: float = 0.0
    ) -> Tuple[str, List[Dict[str, Any]], List[Dict[str, str]]]:
        """
        Execute agent with tool calling loop.
        
        Args:
            model: Model name
            messages: Initial messages
            tools: Tool definitions
            tool_functions: Dict mapping tool names to callable functions
            max_turns: Maximum tool calling iterations
            temperature: Sampling temperature
            
        Returns:
            Tuple of (final_content, all_messages, tool_calls_log)
        """
        tool_calls_log = []
        current_messages = messages.copy()
        
        for turn in range(max_turns):
            # Get completion
            response = self.chat_completion(
                model=model,
                messages=current_messages,
                tools=tools,
                tool_choice="auto",
                temperature=temperature
            )
            
            # Extract assistant message
            if hasattr(response, 'choices'):
                # OpenAI format
                assistant_message = response.choices[0].message
                
                # Check for tool calls
                if hasattr(assistant_message, 'tool_calls') and assistant_message.tool_calls:
                    # Add assistant message to history
                    current_messages.append({
                        "role": "assistant",
                        "content": assistant_message.content,
                        "tool_calls": [
                            {
                                "id": tc.id,
                                "type": "function",
                                "function": {
                                    "name": tc.function.name,
                                    "arguments": tc.function.arguments
                                }
                            }
                            for tc in assistant_message.tool_calls
                        ]
                    })
                    
                    # Execute tools
                    for tool_call in assistant_message.tool_calls:
                        func_name = tool_call.function.name
                        func_args = json.loads(tool_call.function.arguments)
                        
                        # Log the call
                        tool_calls_log.append({
                            "name": func_name,
                            "arguments": str(func_args)
                        })
                        
                        # Execute tool
                        if func_name in tool_functions:
                            tool_result = tool_functions[func_name](**func_args)
                        else:
                            tool_result = json.dumps({"error": f"Unknown tool: {func_name}"})
                        
                        # Add result to messages
                        current_messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": func_name,
                            "content": tool_result
                        })
                else:
                    # No more tool calls - return final answer
                    return assistant_message.content or "", current_messages, tool_calls_log
            else:
                # Anthropic format
                content = response.content[0].text if response.content else ""
                return content, current_messages, tool_calls_log
        
        # Max turns reached
        return "[Max turns reached]", current_messages, tool_calls_log


# Global client instance
_global_client = None


def get_llm_client() -> LLMClient:
    """
    Get or create global LLM client instance.
    
    Returns:
        LLMClient instance
    """
    global _global_client
    if _global_client is None:
        _global_client = LLMClient()
    return _global_client
