"""
AI Orchestrator Module

This module orchestrates the interaction between AI models, secure memory
management, and text-to-speech capabilities. It serves as the central
coordination layer for the Win-Dev-AI framework.

The orchestrator enables:
- Secure AI conversations with automatic memory management
- Voice-enabled AI interactions
- Multi-model support (OpenAI, Anthropic, etc.)
- Context management with encryption
"""

import logging
from typing import Optional, List, Dict, Any, Callable
from datetime import datetime
from .memzero import MemoryManager, SecureMemory
from .azure_tts import AzureTTSEngine

logger = logging.getLogger(__name__)


class ConversationContext:
    """Represents a secure conversation context."""
    
    def __init__(self, memory_manager: MemoryManager, context_id: str):
        """
        Initialize conversation context.
        
        Args:
            memory_manager: The memory manager instance
            context_id: Unique identifier for this context
        """
        self.context_id = context_id
        self.memory_manager = memory_manager
        self.messages: List[Dict[str, str]] = []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        
        # Create secure store for sensitive data
        self._secure_store = memory_manager.create_secure_store(
            f"context_{context_id}"
        )
    
    def add_message(self, role: str, content: str) -> None:
        """
        Add a message to the conversation.
        
        Args:
            role: Message role (user, assistant, system)
            content: Message content
        """
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        self.updated_at = datetime.now()
        logger.debug(f"Added {role} message to context {self.context_id}")
    
    def get_messages(self) -> List[Dict[str, str]]:
        """Get all messages in the conversation."""
        return self.messages.copy()
    
    def clear(self) -> None:
        """Clear all messages and secure data."""
        self.messages.clear()
        self._secure_store.zero()
        logger.info(f"Cleared context {self.context_id}")


class AIOrchestrator:
    """
    Central orchestration system for Win-Dev-AI.
    
    This class coordinates AI models, memory management, and TTS
    to provide a unified AI interaction framework with security
    and voice capabilities.
    """
    
    def __init__(
        self,
        memory_manager: Optional[MemoryManager] = None,
        tts_engine: Optional[AzureTTSEngine] = None,
        enable_voice: bool = False
    ):
        """
        Initialize the AI Orchestrator.
        
        Args:
            memory_manager: MemoryManager instance (created if not provided)
            tts_engine: AzureTTSEngine instance (created if not provided)
            enable_voice: Whether to enable voice output by default
        """
        self.memory_manager = memory_manager or MemoryManager()
        self.tts_engine = tts_engine or AzureTTSEngine()
        self.enable_voice = enable_voice
        
        self._contexts: Dict[str, ConversationContext] = {}
        self._callbacks: Dict[str, List[Callable]] = {
            "on_message": [],
            "on_response": [],
            "on_error": []
        }
        
        logger.info("AIOrchestrator initialized")
    
    def create_context(self, context_id: Optional[str] = None) -> str:
        """
        Create a new conversation context.
        
        Args:
            context_id: Optional custom context ID
            
        Returns:
            The context ID
        """
        if context_id is None:
            context_id = f"ctx_{datetime.now().timestamp()}"
        
        if context_id in self._contexts:
            raise ValueError(f"Context {context_id} already exists")
        
        context = ConversationContext(self.memory_manager, context_id)
        self._contexts[context_id] = context
        logger.info(f"Created context: {context_id}")
        
        return context_id
    
    def get_context(self, context_id: str) -> Optional[ConversationContext]:
        """
        Get a conversation context by ID.
        
        Args:
            context_id: The context identifier
            
        Returns:
            The ConversationContext or None if not found
        """
        return self._contexts.get(context_id)
    
    def delete_context(self, context_id: str) -> bool:
        """
        Delete a conversation context and clear its memory.
        
        Args:
            context_id: The context identifier
            
        Returns:
            True if deleted, False if not found
        """
        if context_id in self._contexts:
            self._contexts[context_id].clear()
            del self._contexts[context_id]
            logger.info(f"Deleted context: {context_id}")
            return True
        return False
    
    def add_message(
        self,
        context_id: str,
        role: str,
        content: str,
        speak: Optional[bool] = None
    ) -> None:
        """
        Add a message to a conversation context.
        
        Args:
            context_id: The context identifier
            role: Message role (user, assistant, system)
            content: Message content
            speak: Whether to speak the message (uses default if None)
        """
        context = self.get_context(context_id)
        if not context:
            raise ValueError(f"Context {context_id} not found")
        
        context.add_message(role, content)
        
        # Trigger callbacks
        for callback in self._callbacks.get("on_message", []):
            try:
                callback(context_id, role, content)
            except Exception as e:
                logger.error(f"Callback error: {e}")
        
        # Speak if enabled and role is assistant
        should_speak = speak if speak is not None else self.enable_voice
        if should_speak and role == "assistant":
            self.speak(content)
    
    def speak(self, text: str, voice: Optional[str] = None) -> bool:
        """
        Speak text using the TTS engine.
        
        Args:
            text: Text to speak
            voice: Optional voice name to use
            
        Returns:
            True if successful, False otherwise
        """
        if voice:
            original_voice = self.tts_engine.default_voice
            self.tts_engine.set_voice(voice)
        
        try:
            result = self.tts_engine.synthesize_to_speaker(text)
            return result
        finally:
            if voice:
                self.tts_engine.set_voice(original_voice)
    
    def save_audio(
        self,
        text: str,
        output_file: str,
        voice: Optional[str] = None
    ) -> bool:
        """
        Save text as audio file.
        
        Args:
            text: Text to convert
            output_file: Path to save audio
            voice: Optional voice name
            
        Returns:
            True if successful, False otherwise
        """
        if voice:
            original_voice = self.tts_engine.default_voice
            self.tts_engine.set_voice(voice)
        
        try:
            result = self.tts_engine.synthesize_to_file(text, output_file)
            return result
        finally:
            if voice:
                self.tts_engine.set_voice(original_voice)
    
    def register_callback(self, event: str, callback: Callable) -> None:
        """
        Register an event callback.
        
        Args:
            event: Event name (on_message, on_response, on_error)
            callback: Callback function
        """
        if event not in self._callbacks:
            raise ValueError(f"Unknown event: {event}")
        
        self._callbacks[event].append(callback)
        logger.info(f"Registered callback for event: {event}")
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """
        Get comprehensive memory and system statistics.
        
        Returns:
            Dictionary containing statistics
        """
        stats = self.memory_manager.get_memory_stats()
        stats['num_contexts'] = len(self._contexts)
        stats['contexts'] = {
            ctx_id: {
                'num_messages': len(ctx.messages),
                'created_at': ctx.created_at.isoformat(),
                'updated_at': ctx.updated_at.isoformat()
            }
            for ctx_id, ctx in self._contexts.items()
        }
        
        return stats
    
    def cleanup(self) -> None:
        """Clean up all resources and zero memory."""
        # Clear all contexts
        for context_id in list(self._contexts.keys()):
            self.delete_context(context_id)
        
        # Zero all memory
        self.memory_manager.zero_all()
        
        logger.info("AIOrchestrator cleanup completed")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cleanup resources."""
        self.cleanup()
        return False
    
    def __del__(self):
        """Destructor - ensure cleanup."""
        self.cleanup()


class AIAssistant:
    """
    High-level AI Assistant interface.
    
    This class provides a simple, user-friendly interface for
    building AI applications with voice and secure memory.
    """
    
    def __init__(
        self,
        name: str = "AI Assistant",
        voice_enabled: bool = False,
        voice_name: Optional[str] = None
    ):
        """
        Initialize the AI Assistant.
        
        Args:
            name: Assistant name
            voice_enabled: Enable voice output
            voice_name: TTS voice name
        """
        self.name = name
        self.orchestrator = AIOrchestrator(enable_voice=voice_enabled)
        
        if voice_name:
            self.orchestrator.tts_engine.set_voice(voice_name)
        
        self.context_id = self.orchestrator.create_context()
        
        # Add system message
        self.orchestrator.add_message(
            self.context_id,
            "system",
            f"You are {name}, a helpful AI assistant."
        )
        
        logger.info(f"AI Assistant '{name}' initialized")
    
    def chat(self, message: str, speak_response: bool = True) -> str:
        """
        Send a message and get a response.
        
        Args:
            message: User message
            speak_response: Whether to speak the response
            
        Returns:
            Assistant response
        """
        # Add user message
        self.orchestrator.add_message(
            self.context_id,
            "user",
            message,
            speak=False
        )
        
        # In a real implementation, this would call an AI model
        # For now, return a placeholder response
        response = f"I received your message: '{message}'. " \
                  f"This is a placeholder response. In production, this would " \
                  f"integrate with OpenAI, Anthropic, or other AI models."
        
        # Add assistant response
        self.orchestrator.add_message(
            self.context_id,
            "assistant",
            response,
            speak=speak_response
        )
        
        return response
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get the full conversation history."""
        context = self.orchestrator.get_context(self.context_id)
        return context.get_messages() if context else []
    
    def clear_history(self) -> None:
        """Clear conversation history."""
        context = self.orchestrator.get_context(self.context_id)
        if context:
            context.clear()
    
    def __del__(self):
        """Cleanup on deletion."""
        self.orchestrator.cleanup()
