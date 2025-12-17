"""
Base Agent
==========
Abstract base class for all agents.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple
from core.utils.llm_client import get_llm_client
from core.utils.config import get_config


class BaseAgent(ABC):
    """
    Abstract base class for all agents.
    
    Features:
    - Message history management
    - Tool integration
    - Model configuration
    - Execution tracking
    """
    
    def __init__(
        self,
        name: str,
        system_prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.0,
        tools: Optional[List[Dict[str, Any]]] = None
    ):
        """
        Initialize agent.
        
        Args:
            name: Agent name
            system_prompt: System instructions
            model: LLM model to use (defaults to config)
            temperature: Sampling temperature
            tools: Tool definitions for function calling
        """
        self.name = name
        self.system_prompt = system_prompt
        self.model = model or get_config().get("default_model")
        self.temperature = temperature
        self.tools = tools or []
        self.tool_functions = {}
        
        # Get LLM client
        self.client = get_llm_client()
        
        # Message history
        self.messages = []
        self._reset_messages()
    
    def _reset_messages(self):
        """Reset message history with system prompt."""
        self.messages = [
            {"role": "system", "content": self.system_prompt}
        ]
    
    def add_tool(self, tool_definition: Dict[str, Any], tool_function: callable):
        """
        Add a tool to the agent.
        
        Args:
            tool_definition: Tool definition dict
            tool_function: Callable that implements the tool
        """
        self.tools.append(tool_definition)
        tool_name = tool_definition.get("function", {}).get("name")
        if tool_name:
            self.tool_functions[tool_name] = tool_function
    
    def add_tools(self, tools: List[Dict[str, Any]], tool_functions: Dict[str, callable]):
        """
        Add multiple tools to the agent.
        
        Args:
            tools: List of tool definitions
            tool_functions: Dict mapping tool names to callables
        """
        self.tools.extend(tools)
        self.tool_functions.update(tool_functions)
    
    def set_model(self, model: str):
        """
        Change the LLM model.
        
        Args:
            model: Model name
        """
        self.model = model
    
    def set_temperature(self, temperature: float):
        """
        Change the temperature.
        
        Args:
            temperature: Sampling temperature (0-1)
        """
        self.temperature = temperature
    
    @abstractmethod
    def run(self, user_input: str, **kwargs) -> str:
        """
        Run the agent with user input.
        
        Args:
            user_input: User's input/query
            **kwargs: Additional arguments
            
        Returns:
            Agent's response
        """
        pass
    
    def _execute_with_tools(
        self,
        user_input: str,
        max_turns: Optional[int] = None
    ) -> Tuple[str, List[Dict[str, str]]]:
        """
        Execute agent with tool calling.
        
        Args:
            user_input: User's input
            max_turns: Maximum tool calling iterations
            
        Returns:
            Tuple of (response, tool_calls_log)
        """
        # Add user message
        self.messages.append({"role": "user", "content": user_input})
        
        # Get max turns from config if not specified
        if max_turns is None:
            max_turns = get_config().get("max_tool_turns", 5)
        
        # Execute tool loop
        response, self.messages, tool_calls = self.client.execute_tool_loop(
            model=self.model,
            messages=self.messages,
            tools=self.tools,
            tool_functions=self.tool_functions,
            max_turns=max_turns,
            temperature=self.temperature
        )
        
        return response, tool_calls
    
    def _execute_simple(self, user_input: str) -> str:
        """
        Execute agent without tools.
        
        Args:
            user_input: User's input
            
        Returns:
            Agent's response
        """
        # Add user message
        self.messages.append({"role": "user", "content": user_input})
        
        # Get completion
        response = self.client.chat_completion(
            model=self.model,
            messages=self.messages,
            temperature=self.temperature
        )
        
        # Extract content
        if hasattr(response, 'choices'):
            content = response.choices[0].message.content
        else:
            content = response.content[0].text if response.content else ""
        
        # Add to history
        self.messages.append({"role": "assistant", "content": content})
        
        return content
    
    def reset(self):
        """Reset the agent's message history."""
        self._reset_messages()
    
    def get_history(self) -> List[Dict[str, Any]]:
        """
        Get message history.
        
        Returns:
            List of messages
        """
        return self.messages.copy()
    
    def reflect(self, output: str, criteria: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Reflect on the agent's output and suggest improvements.
        
        This method allows the agent to self-evaluate its performance
        and identify areas for improvement.
        
        Args:
            output: The agent's output to reflect on
            criteria: Optional list of evaluation criteria
            
        Returns:
            Dict containing:
                - score: Overall quality score (0-10)
                - strengths: List of strengths
                - weaknesses: List of weaknesses
                - improvements: List of suggested improvements
                - revised_output: Improved version (if applicable)
        """
        # Default criteria if not provided
        if criteria is None:
            criteria = [
                "Accuracy and correctness",
                "Completeness of information",
                "Clarity and readability",
                "Relevance to the query",
                "Professional tone"
            ]
        
        # Create reflection prompt
        reflection_prompt = f"""Reflect on the following output and provide a critical analysis:

OUTPUT TO EVALUATE:
{output}

EVALUATION CRITERIA:
{chr(10).join(f'{i+1}. {c}' for i, c in enumerate(criteria))}

Please provide:
1. SCORE: Rate the overall quality (0-10)
2. STRENGTHS: What was done well (2-3 points)
3. WEAKNESSES: What could be improved (2-3 points)
4. IMPROVEMENTS: Specific suggestions for enhancement
5. REVISED OUTPUT: An improved version if significant changes are needed

Format your response as:
SCORE: [number]
STRENGTHS:
- [strength 1]
- [strength 2]
WEAKNESSES:
- [weakness 1]
- [weakness 2]
IMPROVEMENTS:
- [improvement 1]
- [improvement 2]
REVISED OUTPUT:
[improved version or "No major revisions needed"]
"""
        
        # Save current messages
        original_messages = self.messages.copy()
        
        # Reset for reflection
        self._reset_messages()
        
        # Get reflection
        reflection_response = self._execute_simple(reflection_prompt)
        
        # Restore original messages
        self.messages = original_messages
        
        # Parse reflection response
        result = self._parse_reflection(reflection_response)
        result["raw_reflection"] = reflection_response
        
        return result
    
    def _parse_reflection(self, reflection: str) -> Dict[str, Any]:
        """Parse reflection response into structured format."""
        import re
        
        result = {
            "score": 0,
            "strengths": [],
            "weaknesses": [],
            "improvements": [],
            "revised_output": None
        }
        
        try:
            # Extract score
            score_match = re.search(r'SCORE:\s*(\d+(?:\.\d+)?)', reflection, re.IGNORECASE)
            if score_match:
                result["score"] = float(score_match.group(1))
            
            # Extract sections
            sections = {
                "strengths": r'STRENGTHS?:(.*?)(?:WEAKNESSES?:|$)',
                "weaknesses": r'WEAKNESSES?:(.*?)(?:IMPROVEMENTS?:|$)',
                "improvements": r'IMPROVEMENTS?:(.*?)(?:REVISED OUTPUT:|$)',
                "revised_output": r'REVISED OUTPUT:(.*?)$'
            }
            
            for key, pattern in sections.items():
                match = re.search(pattern, reflection, re.IGNORECASE | re.DOTALL)
                if match:
                    content = match.group(1).strip()
                    if key == "revised_output":
                        if "no major revisions" not in content.lower():
                            result[key] = content
                    else:
                        # Extract bullet points
                        items = re.findall(r'[-•]\s*(.+)', content)
                        result[key] = [item.strip() for item in items]
        
        except Exception as e:
            print(f"Warning: Could not parse reflection: {e}")
        
        return result
    
    def run_with_reflection(
        self,
        user_input: str,
        auto_improve: bool = False,
        max_iterations: int = 2,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Run the agent with automatic reflection and optional improvement.
        
        Args:
            user_input: User's input/query
            auto_improve: If True, automatically use improved output
            max_iterations: Maximum improvement iterations
            **kwargs: Additional arguments for run()
            
        Returns:
            Dict containing:
                - output: Final output
                - reflection: Reflection analysis
                - iterations: Number of improvement iterations
        """
        # Initial run
        output = self.run(user_input, **kwargs)
        
        iterations = 0
        reflection = None
        
        if auto_improve:
            for i in range(max_iterations):
                # Reflect on output
                reflection = self.reflect(output)
                
                # Check if improvement is needed
                if reflection["score"] >= 9.0 or not reflection["revised_output"]:
                    break
                
                # Use improved version
                output = reflection["revised_output"]
                iterations = i + 1
        else:
            # Just reflect once
            reflection = self.reflect(output)
        
        return {
            "output": output,
            "reflection": reflection,
            "iterations": iterations
        }
    
    def __repr__(self):
        """String representation."""
        return f"{self.__class__.__name__}(name='{self.name}', model='{self.model}')"
