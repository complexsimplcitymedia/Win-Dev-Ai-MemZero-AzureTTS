"""
Basic Usage Example for Win-Dev-AI-MemZero-AzureTTS

This example demonstrates the core functionality of the framework.
"""

import logging
from win_dev_ai import MemoryManager, AzureTTSEngine, AIOrchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Demonstrate basic usage of Win-Dev-AI framework."""
    
    print("=" * 70)
    print("Win-Dev-AI-MemZero-AzureTTS - Basic Example")
    print("=" * 70)
    
    # 1. Demonstrate Secure Memory Management
    print("\n1. Testing Secure Memory Management...")
    print("-" * 70)
    
    memory_manager = MemoryManager(max_memory_mb=512)
    
    # Create a secure store for sensitive data
    api_key_store = memory_manager.create_secure_store("api_key")
    api_key_store.store("my-super-secret-api-key-12345")
    
    # Retrieve the data
    retrieved_key = api_key_store.retrieve()
    print(f"✓ Stored and retrieved secure data: {retrieved_key[:10]}...")
    
    # Get memory statistics
    stats = memory_manager.get_memory_stats()
    print(f"✓ Memory usage: {stats['rss_mb']:.2f} MB")
    print(f"✓ Secure stores: {stats['num_stores']}")
    
    # Clean up
    memory_manager.delete_secure_store("api_key")
    print("✓ Secure data zeroed from memory")
    
    # 2. Demonstrate Azure TTS Integration
    print("\n2. Testing Azure TTS Integration...")
    print("-" * 70)
    
    tts_engine = AzureTTSEngine()
    
    # List available voices
    voices = tts_engine.get_available_voices()
    print(f"✓ Found {len(voices)} available voices")
    print(f"  Sample voices: {', '.join([v['name'] for v in voices[:3]])}")
    
    # Note: Actual TTS requires Azure credentials
    if tts_engine._speech_config:
        print("✓ Azure TTS configured and ready")
        
        # Create SSML for advanced speech control
        ssml = tts_engine.create_ssml(
            "Hello! This is a test of the Azure Text to Speech integration.",
            rate="medium",
            pitch="medium"
        )
        print("✓ SSML markup created")
    else:
        print("⚠ Azure TTS not configured (set AZURE_SPEECH_KEY environment variable)")
    
    # 3. Demonstrate AI Orchestrator
    print("\n3. Testing AI Orchestrator...")
    print("-" * 70)
    
    with AIOrchestrator(memory_manager=memory_manager, tts_engine=tts_engine) as orchestrator:
        # Create a conversation context
        context_id = orchestrator.create_context("demo_context")
        print(f"✓ Created conversation context: {context_id}")
        
        # Add messages to the context
        orchestrator.add_message(context_id, "system", "You are a helpful assistant.")
        orchestrator.add_message(context_id, "user", "What is AI?")
        orchestrator.add_message(
            context_id,
            "assistant",
            "AI stands for Artificial Intelligence. It refers to computer systems "
            "that can perform tasks that typically require human intelligence."
        )
        
        # Get context information
        context = orchestrator.get_context(context_id)
        if context:
            print(f"✓ Context has {len(context.messages)} messages")
            
        # Get orchestrator statistics
        orchestrator_stats = orchestrator.get_memory_stats()
        print(f"✓ Active contexts: {orchestrator_stats['num_contexts']}")
    
    print("\n✓ Orchestrator cleanup completed (context manager)")
    
    # 4. Demonstrate High-Level AI Assistant
    print("\n4. Testing AI Assistant Interface...")
    print("-" * 70)
    
    from win_dev_ai.ai_orchestrator import AIAssistant
    
    assistant = AIAssistant(
        name="Demo Assistant",
        voice_enabled=False  # Set to True if you have Azure credentials
    )
    
    # Have a conversation
    user_message = "Hello, how are you?"
    print(f"User: {user_message}")
    
    response = assistant.chat(user_message, speak_response=False)
    print(f"Assistant: {response}")
    
    # Get conversation history
    history = assistant.get_conversation_history()
    print(f"✓ Conversation history: {len(history)} messages")
    
    print("\n" + "=" * 70)
    print("Demo completed successfully!")
    print("=" * 70)
    print("\nKey Features Demonstrated:")
    print("  ✓ Secure memory management with automatic zeroing")
    print("  ✓ Azure Text-to-Speech integration")
    print("  ✓ AI orchestration with context management")
    print("  ✓ High-level AI assistant interface")
    print("\nNext Steps:")
    print("  1. Set AZURE_SPEECH_KEY environment variable for TTS")
    print("  2. Set OPENAI_API_KEY for AI model integration")
    print("  3. Explore advanced examples in the examples/ directory")
    print("=" * 70)


if __name__ == "__main__":
    main()
