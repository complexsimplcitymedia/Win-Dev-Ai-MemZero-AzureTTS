"""
Win-Dev-Ai-MemZero-AzureTTS

A revolutionary AI framework combining Windows development capabilities,
secure memory management (MemZero), and Azure Text-to-Speech integration.

This module provides the core functionality for building AI applications
with enhanced security and natural language interfaces.
"""

__version__ = "1.0.0"
__author__ = "ComplexSimplicity Media"

from .memzero import SecureMemory, MemoryManager
from .azure_tts import AzureTTSEngine
from .ai_orchestrator import AIOrchestrator

__all__ = [
    "SecureMemory",
    "MemoryManager",
    "AzureTTSEngine",
    "AIOrchestrator",
]
