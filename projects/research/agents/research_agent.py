"""
Research Agent
=============
Agent specialized in conducting research using various tools.
"""

from typing import Optional, Tuple, List, Dict, Any
from core.agents.base_agent import BaseAgent
from projects.research.tools import (
    tavily_search_tool,
    wikipedia_search_tool,
    arxiv_search_tool,
    get_search_tool_definitions,
    get_academic_tool_definitions
)


class ResearchAgent(BaseAgent):
    """
    Research agent that can use web search and academic tools.
    
    Capabilities:
    - Web search via Tavily
    - Wikipedia lookups
    - Academic paper search via arXiv
    - Multi-source information synthesis
    """
    
    SYSTEM_PROMPT = """You are a research assistant expert in gathering and synthesizing information from multiple sources.

Your capabilities:
1. Web search using Tavily for current information
2. Wikipedia search for encyclopedic knowledge
3. ArXiv search for academic papers

Your process:
1. Break down the research query into sub-questions
2. Use appropriate tools to gather information
3. Synthesize findings from multiple sources
4. Cite sources clearly
5. Provide comprehensive, well-structured answers

Guidelines:
- Use multiple sources to verify information
- Prioritize recent and authoritative sources
- Be critical of information quality
- Cite all sources with URLs
- Format responses in clear markdown
- If information is uncertain, say so
"""
    
    def __init__(
        self,
        model: Optional[str] = None,
        temperature: float = 0.0,
        enable_web_search: bool = True,
        enable_wikipedia: bool = True,
        enable_arxiv: bool = True
    ):
        """
        Initialize research agent.
        
        Args:
            model: LLM model to use
            temperature: Sampling temperature
            enable_web_search: Enable Tavily web search
            enable_wikipedia: Enable Wikipedia search
            enable_arxiv: Enable arXiv academic search
        """
        super().__init__(
            name="ResearchAgent",
            system_prompt=self.SYSTEM_PROMPT,
            model=model,
            temperature=temperature
        )
        
        # Add tools
        tool_functions = {}
        
        if enable_web_search:
            web_tools = get_search_tool_definitions()
            self.add_tools(web_tools, {
                "tavily_search": tavily_search_tool,
                "wikipedia_search": wikipedia_search_tool
            })
        
        if enable_arxiv:
            academic_tools = get_academic_tool_definitions()
            self.add_tools(academic_tools, {
                "arxiv_search": arxiv_search_tool
            })
    
    def run(
        self,
        query: str,
        max_turns: Optional[int] = None,
        return_tool_log: bool = False
    ):
        """
        Conduct research on the given query.
        
        Args:
            query: Research question or topic
            max_turns: Maximum tool calling iterations
            return_tool_log: If True, return (response, tool_log) tuple
            
        Returns:
            Research findings (or tuple with tool log if return_tool_log=True)
        """
        response, tool_log = self._execute_with_tools(query, max_turns)
        
        if return_tool_log:
            return response, tool_log
        return response
    
    def deep_research(
        self,
        topic: str,
        sub_questions: Optional[List[str]] = None,
        max_turns_per_question: int = 3
    ) -> str:
        """
        Conduct deep research by breaking topic into sub-questions.
        
        Args:
            topic: Main research topic
            sub_questions: Optional list of sub-questions to research
            max_turns_per_question: Max tool calls per sub-question
            
        Returns:
            Comprehensive research report
        """
        # Reset for fresh start
        self.reset()
        
        # If no sub-questions provided, ask LLM to generate them
        if not sub_questions:
            planning_prompt = f"""Generate 3-5 specific research sub-questions for the topic: "{topic}"

Format your response as a JSON list of questions:
["Question 1?", "Question 2?", ...]"""
            
            self.messages.append({"role": "user", "content": planning_prompt})
            planning_response = self._execute_simple("")
            
            # Parse sub-questions (simplified parsing)
            import json
            try:
                sub_questions = json.loads(planning_response)
            except:
                # Fallback: just research the main topic
                sub_questions = [topic]
        
        # Research each sub-question
        findings = []
        for i, question in enumerate(sub_questions, 1):
            result = self.run(
                f"Sub-question {i}: {question}",
                max_turns=max_turns_per_question
            )
            findings.append(f"### {question}\n\n{result}")
        
        # Synthesize findings
        synthesis_prompt = f"""Based on the research findings below, create a comprehensive report on "{topic}".

Include:
1. Executive summary
2. Key findings
3. Detailed analysis
4. Sources

Research findings:

{chr(10).join(findings)}"""
        
        self.messages.append({"role": "user", "content": synthesis_prompt})
        final_report = self._execute_simple("")
        
        return final_report


# Convenience function
def create_research_agent(
    model: Optional[str] = None,
    **kwargs
) -> ResearchAgent:
    """
    Create a research agent with default settings.
    
    Args:
        model: LLM model to use
        **kwargs: Additional arguments for ResearchAgent
        
    Returns:
        Configured ResearchAgent instance
    """
    return ResearchAgent(model=model, **kwargs)
