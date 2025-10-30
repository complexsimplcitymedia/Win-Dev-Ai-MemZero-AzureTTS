"""
Tests for AI Orchestrator Module

Testing orchestration and context management.
"""

import pytest
from win_dev_ai.ai_orchestrator import AIOrchestrator, ConversationContext, AIAssistant
from win_dev_ai.memzero import MemoryManager


class TestConversationContext:
    """Test ConversationContext class."""
    
    def test_add_message(self):
        """Test adding messages to context."""
        manager = MemoryManager()
        context = ConversationContext(manager, "test_ctx")
        
        context.add_message("user", "Hello")
        context.add_message("assistant", "Hi there!")
        
        messages = context.get_messages()
        assert len(messages) == 2
        assert messages[0]['role'] == "user"
        assert messages[1]['content'] == "Hi there!"
    
    def test_clear(self):
        """Test clearing context."""
        manager = MemoryManager()
        context = ConversationContext(manager, "test_ctx")
        
        context.add_message("user", "Test")
        context.clear()
        
        assert len(context.messages) == 0


class TestAIOrchestrator:
    """Test AIOrchestrator class."""
    
    def test_create_context(self):
        """Test creating a conversation context."""
        orchestrator = AIOrchestrator()
        
        ctx_id = orchestrator.create_context("test_context")
        
        assert ctx_id == "test_context"
        assert orchestrator.get_context(ctx_id) is not None
    
    def test_auto_generated_context_id(self):
        """Test auto-generated context IDs."""
        orchestrator = AIOrchestrator()
        
        ctx_id = orchestrator.create_context()
        
        assert ctx_id is not None
        assert orchestrator.get_context(ctx_id) is not None
    
    def test_delete_context(self):
        """Test deleting a context."""
        orchestrator = AIOrchestrator()
        ctx_id = orchestrator.create_context("to_delete")
        
        result = orchestrator.delete_context(ctx_id)
        
        assert result is True
        assert orchestrator.get_context(ctx_id) is None
    
    def test_add_message_to_context(self):
        """Test adding messages to a context."""
        orchestrator = AIOrchestrator()
        ctx_id = orchestrator.create_context()
        
        orchestrator.add_message(ctx_id, "user", "Hello")
        
        context = orchestrator.get_context(ctx_id)
        assert len(context.messages) == 1
    
    def test_context_manager(self):
        """Test orchestrator as context manager."""
        with AIOrchestrator() as orchestrator:
            ctx_id = orchestrator.create_context()
            orchestrator.add_message(ctx_id, "user", "Test")
            
            assert len(orchestrator._contexts) == 1
        
        # After exit, contexts should be cleaned up
        # (orchestrator is out of scope, cleanup called)
    
    def test_memory_stats(self):
        """Test getting memory statistics."""
        orchestrator = AIOrchestrator()
        ctx_id1 = orchestrator.create_context()
        ctx_id2 = orchestrator.create_context()
        
        stats = orchestrator.get_memory_stats()
        
        assert stats['num_contexts'] == 2
        assert ctx_id1 in stats['contexts']
        assert ctx_id2 in stats['contexts']
    
    def test_callback_registration(self):
        """Test callback registration."""
        orchestrator = AIOrchestrator()
        
        callback_called = []
        
        def test_callback(ctx_id, role, content):
            callback_called.append((ctx_id, role, content))
        
        orchestrator.register_callback("on_message", test_callback)
        
        ctx_id = orchestrator.create_context()
        orchestrator.add_message(ctx_id, "user", "Test message")
        
        assert len(callback_called) == 1
        assert callback_called[0][2] == "Test message"


class TestAIAssistant:
    """Test AIAssistant class."""
    
    def test_initialization(self):
        """Test assistant initialization."""
        assistant = AIAssistant(name="TestBot")
        
        assert assistant.name == "TestBot"
        assert assistant.context_id is not None
    
    def test_chat(self):
        """Test chat functionality."""
        assistant = AIAssistant()
        
        response = assistant.chat("Hello", speak_response=False)
        
        assert response is not None
        assert len(response) > 0
    
    def test_conversation_history(self):
        """Test getting conversation history."""
        assistant = AIAssistant()
        
        assistant.chat("First message", speak_response=False)
        assistant.chat("Second message", speak_response=False)
        
        history = assistant.get_conversation_history()
        
        # Should have system message + 2 user messages + 2 assistant responses
        assert len(history) >= 4
    
    def test_clear_history(self):
        """Test clearing conversation history."""
        assistant = AIAssistant()
        
        assistant.chat("Test", speak_response=False)
        assistant.clear_history()
        
        history = assistant.get_conversation_history()
        assert len(history) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
