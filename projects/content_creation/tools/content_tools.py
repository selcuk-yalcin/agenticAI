"""
Content Creation Tools
=====================
Tools for keyword research and SEO optimization.
"""

import json
from typing import Dict, Any, List
from core.tools import BaseTool


class KeywordResearchTool(BaseTool):
    """
    Simulated keyword research tool.
    In production, integrate with real SEO APIs (SEMrush, Ahrefs, etc.)
    """
    
    def __init__(self):
        super().__init__(
            name="keyword_research",
            description="Research keywords related to a topic for SEO optimization"
        )
    
    def execute(self, topic: str, num_keywords: int = 10) -> str:
        """
        Research keywords for a topic.
        
        Args:
            topic: Topic to research
            num_keywords: Number of keywords to return
            
        Returns:
            JSON string with keyword data
        """
        try:
            # In production, integrate with real API
            # This is a simplified simulation
            keywords = self._simulate_keywords(topic, num_keywords)
            
            return self.format_success({
                "topic": topic,
                "keywords": keywords,
                "count": len(keywords)
            })
            
        except Exception as e:
            return self.format_error(str(e))
    
    def _simulate_keywords(self, topic: str, count: int) -> List[Dict[str, Any]]:
        """Simulate keyword research results."""
        # In production, call real API
        base_keywords = [
            f"{topic} guide",
            f"best {topic}",
            f"{topic} tips",
            f"how to {topic}",
            f"{topic} examples",
            f"{topic} tutorial",
            f"{topic} benefits",
            f"{topic} strategies",
            f"{topic} tools",
            f"{topic} best practices"
        ]
        
        return [
            {
                "keyword": kw,
                "search_volume": "1000-10000",
                "difficulty": "medium",
                "intent": "informational"
            }
            for kw in base_keywords[:count]
        ]
    
    @property
    def tool_definition(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "topic": {
                            "type": "string",
                            "description": "Topic to research keywords for"
                        },
                        "num_keywords": {
                            "type": "integer",
                            "description": "Number of keywords to return (default: 10)"
                        }
                    },
                    "required": ["topic"]
                }
            }
        }


class SEOOptimizerTool(BaseTool):
    """
    Tool for SEO optimization suggestions.
    """
    
    def __init__(self):
        super().__init__(
            name="seo_optimizer",
            description="Analyze content and provide SEO optimization suggestions"
        )
    
    def execute(self, content: str, target_keywords: List[str] = None) -> str:
        """
        Analyze content for SEO.
        
        Args:
            content: Content to analyze
            target_keywords: Target keywords to check
            
        Returns:
            JSON string with SEO analysis
        """
        try:
            analysis = {
                "word_count": len(content.split()),
                "readability": "good",
                "keyword_density": {},
                "suggestions": []
            }
            
            # Analyze keyword density
            if target_keywords:
                content_lower = content.lower()
                for keyword in target_keywords:
                    count = content_lower.count(keyword.lower())
                    density = (count / len(content.split())) * 100
                    analysis["keyword_density"][keyword] = {
                        "count": count,
                        "density": f"{density:.2f}%"
                    }
            
            # Generate suggestions
            if analysis["word_count"] < 300:
                analysis["suggestions"].append("Consider adding more content (minimum 300 words)")
            
            if target_keywords:
                for kw, data in analysis["keyword_density"].items():
                    if data["count"] == 0:
                        analysis["suggestions"].append(f"Add target keyword: '{kw}'")
                    elif data["count"] > 10:
                        analysis["suggestions"].append(f"Reduce keyword '{kw}' usage (avoid keyword stuffing)")
            
            # Check for headings
            if "##" not in content and "#" not in content:
                analysis["suggestions"].append("Add headings (H2, H3) for better structure")
            
            return self.format_success(analysis)
            
        except Exception as e:
            return self.format_error(str(e))
    
    @property
    def tool_definition(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "content": {
                            "type": "string",
                            "description": "Content to analyze for SEO"
                        },
                        "target_keywords": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of target keywords to check"
                        }
                    },
                    "required": ["content"]
                }
            }
        }


# Singleton instances
keyword_research_tool = KeywordResearchTool()
seo_optimizer_tool = SEOOptimizerTool()

# Registry
CONTENT_TOOLS = {
    "keyword_research": keyword_research_tool.tool_definition,
    "seo_optimizer": seo_optimizer_tool.tool_definition
}


def get_content_tool_definitions() -> list:
    """Get all content tool definitions for LLM."""
    return list(CONTENT_TOOLS.values())
