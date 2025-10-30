"""
Memory Agent - Model-Agnostic AI Agent
Integrates with MCP and provides universal memory capabilities.
"""

import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

from .memory import UniversalMemory, MemoryRetriever

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MemoryAgent:
    """
    Model-agnostic AI agent with universal memory capabilities.
    Works with any AI model through the MCP architecture.
    """
    
    def __init__(self, agent_id: str, memory_path: Optional[Path] = None):
        self.agent_id = agent_id
        self.memory = UniversalMemory(memory_path)
        self.retriever = MemoryRetriever(self.memory)
        
        # Agent state
        self.conversation_history: List[Dict[str, str]] = []
        self.current_context: Optional[str] = None
        
        logger.info(f"Memory Agent '{agent_id}' initialized")
    
    def process_input(self, user_input: str, model_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Process user input with memory augmentation.
        Model-agnostic - works with any AI model.
        
        Args:
            user_input: User's input message
            model_name: Optional AI model name (for logging)
        
        Returns:
            Processing results with context and memories
        """
        # Store user input as memory
        memory_id = self.memory.store(
            content=f"User: {user_input}",
            metadata={"type": "user_input", "model": model_name or "unknown"},
            importance=0.8,
            tags=["conversation", "user"]
        )
        
        # Retrieve relevant context
        context = self.retriever.get_context(user_input, max_tokens=4000)
        self.current_context = context
        
        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_input,
            "memory_id": memory_id
        })
        
        logger.info(f"Processed input for agent '{self.agent_id}' using model '{model_name}'")
        
        return {
            "agent_id": self.agent_id,
            "input": user_input,
            "context": context,
            "memory_id": memory_id,
            "model": model_name
        }
    
    def process_response(self, response: str, model_name: Optional[str] = None) -> str:
        """
        Process AI response and store it in memory.
        
        Args:
            response: AI's response
            model_name: Optional AI model name
        
        Returns:
            Memory ID of stored response
        """
        memory_id = self.memory.store(
            content=f"Assistant: {response}",
            metadata={"type": "assistant_response", "model": model_name or "unknown"},
            importance=0.7,
            tags=["conversation", "assistant"]
        )
        
        # Add to conversation history
        self.conversation_history.append({
            "role": "assistant",
            "content": response,
            "memory_id": memory_id,
            "model": model_name
        })
        
        return memory_id
    
    def remember(self, content: str, importance: float = 1.0, 
                tags: Optional[List[str]] = None) -> str:
        """
        Store a memory with custom importance and tags.
        
        Args:
            content: Content to remember
            importance: Importance score (0.0 to 1.0)
            tags: Optional list of tags
        
        Returns:
            Memory ID
        """
        return self.memory.store(
            content=content,
            metadata={"agent_id": self.agent_id},
            importance=importance,
            tags=tags or []
        )
    
    def recall(self, query: str, limit: int = 10) -> List[str]:
        """
        Recall memories related to a query.
        
        Args:
            query: Search query
            limit: Maximum number of results
        
        Returns:
            List of memory contents
        """
        memories = self.memory.search(query, limit=limit)
        return [m.content for m in memories]
    
    def get_conversation_context(self, max_messages: int = 10) -> str:
        """
        Get recent conversation context.
        
        Args:
            max_messages: Maximum number of messages to include
        
        Returns:
            Formatted conversation context
        """
        recent_history = self.conversation_history[-max_messages:]
        context_parts = []
        
        for msg in recent_history:
            role = msg["role"].capitalize()
            content = msg["content"]
            context_parts.append(f"{role}: {content}")
        
        return "\n".join(context_parts)
    
    def clear_conversation(self):
        """Clear the conversation history (but keep memories)."""
        self.conversation_history = []
        logger.info(f"Cleared conversation history for agent '{self.agent_id}'")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get agent statistics."""
        memory_stats = self.memory.get_stats()
        
        return {
            "agent_id": self.agent_id,
            "conversation_length": len(self.conversation_history),
            "memory_stats": memory_stats,
            "has_context": self.current_context is not None
        }
    
    def integrate_with_mcp(self, mcp_instance, service_name: Optional[str] = None):
        """
        Integrate this agent with MCP.
        
        Args:
            mcp_instance: MasterControlProgram instance
            service_name: Optional custom service name
        """
        from mcp.core import ServiceConfig
        
        service_name = service_name or f"memory_agent_{self.agent_id}"
        
        service = ServiceConfig(
            name=service_name,
            service_type="memory_agent",
            endpoint=f"agent://{self.agent_id}",
            enabled=True,
            metadata={
                "agent_id": self.agent_id,
                "capabilities": ["memory", "retrieval", "conversation"]
            }
        )
        
        mcp_instance.register_service(service)
        logger.info(f"Agent '{self.agent_id}' integrated with MCP as '{service_name}'")
