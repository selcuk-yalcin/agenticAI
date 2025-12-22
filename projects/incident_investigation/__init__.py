"""
AI-Powered Incident Investigation System

A comprehensive incident investigation platform for high-risk industries including
oil & gas, petrochemicals, energy, mining, and defense.

Modules:
    - agents: Specialized AI agents for investigation workflow
    - core: Root cause taxonomies and frameworks
    - examples: Usage examples and demonstrations

Version: 1.0.0
Author: AI Development Team
"""

__version__ = "1.0.0"
__author__ = "AI Development Team"

from .agents.orchestrator import IncidentOrchestrator

__all__ = [
    "IncidentOrchestrator",
]
