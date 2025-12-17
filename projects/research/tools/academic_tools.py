"""
Academic Tools
==============
Tools for searching academic papers and publications.
"""

import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from typing import Dict, Any
from core.tools.base_tool import BaseTool


class ArxivSearchTool(BaseTool):
    """
    arXiv search tool.
    
    Searches arXiv.org for academic papers in supported domains.
    No API key required - uses public arXiv API.
    
    Supported domains:
    - Computer Science (cs)
    - Mathematics (math)
    - Physics (physics)
    - Statistics (stat)
    - Quantitative Biology (q-bio)
    - Quantitative Finance (q-fin)
    - Electrical Engineering (eess)
    - Economics (econ)
    """
    
    def __init__(self):
        super().__init__(
            name="arxiv_search",
            description="Search arXiv.org for academic papers in CS, Math, Physics, and related fields"
        )
    
    def execute(self, query: str, max_results: int = 5) -> str:
        """
        Execute arXiv search.
        
        Args:
            query: Academic search query
            max_results: Maximum papers to return
            
        Returns:
            JSON string with paper details
        """
        try:
            # Encode query
            encoded_query = urllib.parse.quote(query)
            url = f"http://export.arxiv.org/api/query?search_query=all:{encoded_query}&start=0&max_results={max_results}"
            
            # Fetch results
            with urllib.request.urlopen(url) as response:
                data = response.read().decode('utf-8')
            
            # Parse XML
            root = ET.fromstring(data)
            namespace = {'atom': 'http://www.w3.org/2005/Atom'}
            
            results = []
            for entry in root.findall('atom:entry', namespace):
                title = entry.find('atom:title', namespace)
                summary = entry.find('atom:summary', namespace)
                published = entry.find('atom:published', namespace)
                link = entry.find('atom:id', namespace)
                
                # Get authors
                authors = []
                for author in entry.findall('atom:author', namespace):
                    name = author.find('atom:name', namespace)
                    if name is not None:
                        authors.append(name.text)
                
                # Get categories
                categories = []
                for category in entry.findall('atom:category', namespace):
                    term = category.get('term')
                    if term:
                        categories.append(term)
                
                results.append({
                    "title": title.text.strip() if title is not None else "",
                    "authors": authors,
                    "summary": summary.text.strip() if summary is not None else "",
                    "published": published.text if published is not None else "",
                    "url": link.text if link is not None else "",
                    "categories": categories
                })
            
            return self.format_success(
                data=results,
                query=query,
                total_results=len(results),
                source="arXiv.org"
            )
            
        except Exception as e:
            return self.format_error(
                e,
                query=query,
                help="Check internet connection and query format"
            )
    
    @property
    def tool_definition(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Search arXiv.org for academic papers. ONLY use for Computer Science, Mathematics, Physics, Statistics, Biology, Finance, Engineering, or Economics topics.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Academic search query for papers"
                        },
                        "max_results": {
                            "type": "integer",
                            "description": "Maximum papers to return (default: 5)",
                            "default": 5
                        }
                    },
                    "required": ["query"]
                }
            }
        }


# Create singleton instance
arxiv_search_tool = ArxivSearchTool()


# Tool registry
ACADEMIC_TOOLS = {
    "arxiv_search": arxiv_search_tool
}


def get_academic_tool_definitions():
    """Get all academic tool definitions for LLM function calling."""
    return [tool.tool_definition for tool in ACADEMIC_TOOLS.values()]
