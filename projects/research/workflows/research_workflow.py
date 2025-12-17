"""
Research Workflow
Multi-step research process with verification and synthesis
"""

from typing import Dict, Any, List
from ..agents.research_agent import ResearchAgent


class ResearchWorkflow:
    """Orchestrates multi-step research tasks."""
    
    def __init__(self):
        self.agent = ResearchAgent()
        self.research_history = []
    
    def comprehensive_research(
        self,
        topic: str,
        depth: str = "medium"
    ) -> Dict[str, Any]:
        """
        Conduct comprehensive research on a topic.
        
        Args:
            topic: Research topic
            depth: Research depth (light, medium, deep)
        
        Returns:
            Comprehensive research report
        """
        print(f"Starting comprehensive research on: {topic}")
        
        # Step 1: Initial overview
        print("Step 1: Getting overview...")
        overview = self.agent.run(f"Provide an overview of {topic}")
        
        # Step 2: Web search for current information
        print("Step 2: Searching current information...")
        current_info = self.agent.run(
            f"Search latest information about {topic}",
            use_tools=True
        )
        
        # Step 3: Academic perspective (if deep research)
        academic_info = None
        if depth in ["medium", "deep"]:
            print("Step 3: Finding academic sources...")
            academic_info = self.agent.run(
                f"Find academic papers about {topic}",
                use_tools=True
            )
        
        # Step 4: Synthesis
        print("Step 4: Synthesizing findings...")
        synthesis_prompt = f"""Synthesize research on {topic}:

Overview: {overview}
Current Information: {current_info}
Academic Sources: {academic_info if academic_info else "N/A"}

Provide:
1. Executive summary
2. Key findings
3. Current trends
4. Academic insights
5. Practical applications
6. Future outlook"""
        
        synthesis = self.agent.run(synthesis_prompt)
        
        result = {
            "topic": topic,
            "depth": depth,
            "overview": overview,
            "current_info": current_info,
            "academic_info": academic_info,
            "synthesis": synthesis,
            "sources_used": self._extract_sources()
        }
        
        self.research_history.append(result)
        return result
    
    def comparative_research(
        self,
        topics: List[str],
        comparison_criteria: List[str] = None
    ) -> Dict[str, Any]:
        """
        Compare multiple topics side-by-side.
        
        Args:
            topics: List of topics to compare
            comparison_criteria: Criteria for comparison
        
        Returns:
            Comparative analysis
        """
        if comparison_criteria is None:
            comparison_criteria = [
                "popularity", "effectiveness", "cost",
                "ease of use", "future potential"
            ]
        
        print(f"Comparing {len(topics)} topics...")
        
        # Research each topic
        topic_research = {}
        for topic in topics:
            print(f"Researching: {topic}")
            research = self.agent.run(f"Research {topic}")
            topic_research[topic] = research
        
        # Generate comparison
        comparison_prompt = f"""Compare these topics:

Topics: {', '.join(topics)}
Criteria: {', '.join(comparison_criteria)}

Research data:
{chr(10).join([f'{t}: {r[:200]}...' for t, r in topic_research.items()])}

Provide comparison table and analysis."""
        
        comparison = self.agent.run(comparison_prompt)
        
        return {
            "topics": topics,
            "criteria": comparison_criteria,
            "individual_research": topic_research,
            "comparison": comparison
        }
    
    def trend_analysis(
        self,
        topic: str,
        time_period: str = "last_year"
    ) -> Dict[str, Any]:
        """
        Analyze trends for a topic over time.
        
        Args:
            topic: Topic to analyze
            time_period: Time period to analyze
        
        Returns:
            Trend analysis report
        """
        print(f"Analyzing trends for: {topic}")
        
        # Current state
        current = self.agent.run(f"Current state of {topic}")
        
        # Historical context
        historical = self.agent.run(f"History and evolution of {topic}")
        
        # Future predictions
        future = self.agent.run(f"Future predictions for {topic}")
        
        # Synthesis
        trend_prompt = f"""Analyze trends for {topic} over {time_period}:

Current State: {current}
Historical Context: {historical}
Future Predictions: {future}

Provide:
1. Timeline of key developments
2. Growth patterns
3. Emerging trends
4. Decline indicators
5. Future trajectory"""
        
        analysis = self.agent.run(trend_prompt)
        
        return {
            "topic": topic,
            "time_period": time_period,
            "current_state": current,
            "historical_context": historical,
            "future_outlook": future,
            "trend_analysis": analysis
        }
    
    def expert_synthesis(
        self,
        topic: str,
        perspectives: List[str] = None
    ) -> Dict[str, Any]:
        """
        Synthesize expert perspectives on a topic.
        
        Args:
            topic: Topic to research
            perspectives: Expert perspectives to include
        
        Returns:
            Multi-perspective synthesis
        """
        if perspectives is None:
            perspectives = [
                "technical", "business", "social",
                "ethical", "economic"
            ]
        
        print(f"Gathering expert perspectives on: {topic}")
        
        perspective_research = {}
        for perspective in perspectives:
            print(f"Analyzing {perspective} perspective...")
            research = self.agent.run(
                f"Analyze {topic} from {perspective} perspective"
            )
            perspective_research[perspective] = research
        
        # Synthesize all perspectives
        synthesis_prompt = f"""Synthesize expert perspectives on {topic}:

Perspectives analyzed: {', '.join(perspectives)}

{chr(10).join([f'{p.upper()}: {r[:150]}...' for p, r in perspective_research.items()])}

Provide integrated analysis considering all perspectives."""
        
        synthesis = self.agent.run(synthesis_prompt)
        
        return {
            "topic": topic,
            "perspectives": perspectives,
            "perspective_research": perspective_research,
            "synthesis": synthesis
        }
    
    def _extract_sources(self) -> List[str]:
        """Extract sources from agent's message history."""
        sources = []
        for msg in self.agent.messages:
            if "source" in msg.get("content", "").lower():
                sources.append(msg["content"])
        return sources
    
    def get_research_history(self) -> List[Dict[str, Any]]:
        """Get all research conducted in this session."""
        return self.research_history


def create_research_workflow() -> ResearchWorkflow:
    """Factory function to create a ResearchWorkflow."""
    return ResearchWorkflow()
