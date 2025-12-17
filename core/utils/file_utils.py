"""
File Utilities
=============
Helper functions for file I/O operations.
"""

import os
import json
import csv
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime


def ensure_directory(path: str) -> Path:
    """
    Ensure directory exists, create if it doesn't.
    
    Args:
        path: Directory path
        
    Returns:
        Path object
    """
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def save_markdown(content: str, filename: str, output_dir: str = "./outputs") -> str:
    """
    Save content as markdown file.
    
    Args:
        content: Markdown content
        filename: Output filename (without extension)
        output_dir: Output directory
        
    Returns:
        Full path to saved file
    """
    ensure_directory(output_dir)
    
    # Add timestamp if filename already exists
    filepath = Path(output_dir) / f"{filename}.md"
    if filepath.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = Path(output_dir) / f"{filename}_{timestamp}.md"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return str(filepath)


def save_json(data: Any, filename: str, output_dir: str = "./outputs") -> str:
    """
    Save data as JSON file.
    
    Args:
        data: Data to save
        filename: Output filename (without extension)
        output_dir: Output directory
        
    Returns:
        Full path to saved file
    """
    ensure_directory(output_dir)
    
    filepath = Path(output_dir) / f"{filename}.json"
    if filepath.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = Path(output_dir) / f"{filename}_{timestamp}.json"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return str(filepath)


def save_csv(data: List[Dict[str, Any]], filename: str, output_dir: str = "./outputs") -> str:
    """
    Save data as CSV file.
    
    Args:
        data: List of dictionaries
        filename: Output filename (without extension)
        output_dir: Output directory
        
    Returns:
        Full path to saved file
    """
    if not data:
        raise ValueError("Cannot save empty data to CSV")
    
    ensure_directory(output_dir)
    
    filepath = Path(output_dir) / f"{filename}.csv"
    if filepath.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = Path(output_dir) / f"{filename}_{timestamp}.csv"
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    
    return str(filepath)


def load_json(filepath: str) -> Any:
    """
    Load JSON file.
    
    Args:
        filepath: Path to JSON file
        
    Returns:
        Loaded data
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_markdown(filepath: str) -> str:
    """
    Load markdown file.
    
    Args:
        filepath: Path to markdown file
        
    Returns:
        File content
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def load_csv(filepath: str) -> List[Dict[str, Any]]:
    """
    Load CSV file.
    
    Args:
        filepath: Path to CSV file
        
    Returns:
        List of dictionaries
    """
    with open(filepath, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)


def format_markdown_report(
    title: str,
    sections: Dict[str, str],
    metadata: Optional[Dict[str, Any]] = None
) -> str:
    """
    Format a structured markdown report.
    
    Args:
        title: Report title
        sections: Dictionary of section name -> content
        metadata: Optional metadata to include at top
        
    Returns:
        Formatted markdown string
    """
    lines = [f"# {title}\n"]
    
    # Add metadata if provided
    if metadata:
        lines.append("## Metadata\n")
        for key, value in metadata.items():
            lines.append(f"- **{key}**: {value}")
        lines.append("")
    
    # Add sections
    for section_name, content in sections.items():
        lines.append(f"## {section_name}\n")
        lines.append(content)
        lines.append("")
    
    return "\n".join(lines)


def get_timestamp() -> str:
    """
    Get current timestamp string.
    
    Returns:
        Timestamp in format YYYYMMDD_HHMMSS
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing invalid characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename
