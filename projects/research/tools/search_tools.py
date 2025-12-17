"""
Search Tools
============
Web and encyclopedia search tools.
"""

import os
import json
import urllib.request
import urllib.parse
from typing import Dict, Any
from core.tools.base_tool import BaseTool


class TavilySearchTool(BaseTool):
    """
    Tavily web search tool.
    
    Searches the web for recent information, news, and general content.
    Requires TAVILY_API_KEY environment variable.
    """
    
    def __init__(self):
        super().__init__(
            name="tavily_search",
            description="Search the web for recent information, news, blogs, and general content"
        )
    
    def execute(self, query: str, max_results: int = 5) -> str:
        """
        Execute Tavily web search.
        
        Args:
            query: Search query
            max_results: Maximum results to return
            
        Returns:
            JSON string with search results
        """
        try:
            # Check if tavily is available
            try:
                from tavily import TavilyClient
            except ImportError:
                return self.format_error(
                    Exception("tavily-python not installed"),
                    help="Install with: pip install tavily-python"
                )
            
            # Get API key
            api_key = os.getenv("TAVILY_API_KEY")
            if not api_key:
                return self.format_error(
                    Exception("TAVILY_API_KEY not found"),
                    help="Get your key from https://tavily.com"
                )
            
            # Perform search
            client = TavilyClient(api_key=api_key)
            response = client.search(query=query, max_results=max_results)
            
            # Format results
            results = []
            for item in response.get("results", []):
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "content": item.get("content", ""),
                    "score": item.get("score", 0)
                })
            
            return self.format_success(
                data=results,
                query=query,
                total_results=len(results),
                source="Tavily"
            )
            
        except Exception as e:
            return self.format_error(e, query=query)
    
    @property
    def tool_definition(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Search the web for recent information, news, blogs, and general content. Use for current events, practical guides, and non-academic sources.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query string"
                        },
                        "max_results": {
                            "type": "integer",
                            "description": "Maximum number of results (default: 5)",
                            "default": 5
                        }
                    },
                    "required": ["query"]
                }
            }
        }


class WikipediaSearchTool(BaseTool):
    """
    Wikipedia search tool.
    
    Searches Wikipedia for encyclopedic information and definitions.
    No API key required - uses public Wikipedia API.
    """
    
    def __init__(self):
        super().__init__(
            name="wikipedia_search",
            description="Search Wikipedia for encyclopedic information and definitions"
        )
    
    def execute(self, query: str) -> str:
        """
        Execute Wikipedia search.
        
        Args:
            query: Search query (article title or topic)
            
        Returns:
            JSON string with article summary
        """
        try:
            base_url = "https://en.wikipedia.org/w/api.php"
            
            # Search for article
            search_params = {
                "action": "query",
                "list": "search",
                "srsearch": query,
                "format": "json",
                "srlimit": 1
            }
            
            search_url = base_url + "?" + urllib.parse.urlencode(search_params)
            
            with urllib.request.urlopen(search_url) as response:
                search_data = json.loads(response.read().decode('utf-8'))
            
            if not search_data.get("query", {}).get("search"):
                return self.format_error(
                    Exception("No results found"),
                    query=query,
                    suggestion="Try different keywords"
                )
            
            # Get first result
            page_title = search_data["query"]["search"][0]["title"]
            page_id = search_data["query"]["search"][0]["pageid"]
            
            # Get article extract
            extract_params = {
                "action": "query",
                "prop": "extracts|info",
                "pageids": page_id,
                "exintro": True,
                "explaintext": True,
                "inprop": "url",
                "format": "json"
            }
            
            extract_url = base_url + "?" + urllib.parse.urlencode(extract_params)
            
            with urllib.request.urlopen(extract_url) as response:
                extract_data = json.loads(response.read().decode('utf-8'))
            
            page_data = extract_data["query"]["pages"][str(page_id)]
            
            return self.format_success(
                data={
                    "title": page_data.get("title", ""),
                    "summary": page_data.get("extract", ""),
                    "url": page_data.get("fullurl", "")
                },
                query=query,
                source="Wikipedia"
            )
            
        except Exception as e:
            return self.format_error(e, query=query)
    
    @property
    def tool_definition(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Search Wikipedia for encyclopedic information, definitions, historical context, and background knowledge.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Wikipedia article title or topic to search"
                        }
                    },
                    "required": ["query"]
                }
            }
        }


# Create singleton instances
tavily_search_tool = TavilySearchTool()
wikipedia_search_tool = WikipediaSearchTool()


# Tool registry for easy access
SEARCH_TOOLS = {
    "tavily_search": tavily_search_tool,
    "wikipedia_search": wikipedia_search_tool
}


def get_search_tool_definitions():
    """Get all search tool definitions for LLM function calling."""
    return [tool.tool_definition for tool in SEARCH_TOOLS.values()]
