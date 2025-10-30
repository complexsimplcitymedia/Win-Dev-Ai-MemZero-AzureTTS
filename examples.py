"""
Example: Using the Universal Memory System
This example demonstrates how to use the system with any AI model.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from mcp.core import MasterControlProgram
from agents.agent import MemoryAgent
from tts_bridge.bridge import TTSBridge
from ollama_config.manager import OllamaManager


def example_memory_agent():
    """Example: Using the Memory Agent with any AI model."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Memory Agent with Model-Agnostic Design")
    print("="*60)
    
    # Create a memory agent
    agent = MemoryAgent("demo_agent")
    
    # Simulate conversation with ANY AI model
    # The system doesn't care which model you use!
    
    print("\n--- Using GPT-4 ---")
    user_input = "What is the capital of France?"
    result = agent.process_input(user_input, model_name="gpt-4")
    print(f"User: {user_input}")
    
    # Simulate AI response (in real use, this comes from your AI model)
    ai_response = "The capital of France is Paris."
    agent.process_response(ai_response, model_name="gpt-4")
    print(f"GPT-4: {ai_response}")
    
    print("\n--- Switching to Claude ---")
    user_input = "Tell me more about Paris."
    result = agent.process_input(user_input, model_name="claude-2")
    print(f"User: {user_input}")
    
    # The agent retrieves context from previous conversation!
    print(f"Context retrieved: {len(result['context'])} characters")
    
    ai_response = "Paris is the largest city in France and a major European city."
    agent.process_response(ai_response, model_name="claude-2")
    print(f"Claude: {ai_response}")
    
    print("\n--- Switching to Llama ---")
    user_input = "What did we discuss about France?"
    result = agent.process_input(user_input, model_name="llama2")
    print(f"User: {user_input}")
    
    # Memory persists across model switches!
    recalled = agent.recall("France", limit=3)
    print(f"Recalled memories: {len(recalled)}")
    for i, mem in enumerate(recalled, 1):
        print(f"  {i}. {mem[:60]}...")
    
    # Get statistics
    stats = agent.get_stats()
    print(f"\nAgent Statistics:")
    print(f"  Conversation Length: {stats['conversation_length']} messages")
    print(f"  Total Memories: {stats['memory_stats']['total_memories']}")


def example_mcp_integration():
    """Example: Integrating all components with MCP."""
    print("\n" + "="*60)
    print("EXAMPLE 2: MCP Integration - Single Source of Truth")
    print("="*60)
    
    # Initialize MCP
    mcp = MasterControlProgram()
    mcp.start()
    print("\nMCP initialized and started")
    
    # Register all components with MCP
    agent = MemoryAgent("integrated_agent")
    agent.integrate_with_mcp(mcp, "agent_service")
    print("✓ Memory Agent integrated")
    
    tts = TTSBridge()
    tts.integrate_with_mcp(mcp, "tts_service")
    print("✓ TTS Bridge integrated")
    
    ollama = OllamaManager()
    ollama.integrate_with_mcp(mcp, "ollama_service")
    print("✓ Ollama Manager integrated")
    
    # Check MCP status
    status = mcp.get_status()
    print(f"\nMCP Status:")
    print(f"  Running: {status['running']}")
    print(f"  Services: {status['services']}")
    print(f"  Registered: {', '.join(status['service_list'])}")
    
    # Save configuration
    config_file = Path("example_mcp_config.json")
    mcp.save_config(config_file)
    print(f"\n✓ Configuration saved to {config_file}")
    
    # Route a request through MCP
    from mcp.core import GatewayConfig
    gateway = GatewayConfig(
        name="example_gateway",
        gateway_type="router",
        target_services=["agent_service"]
    )
    mcp.register_gateway(gateway)
    
    result = mcp.route_request("example_gateway", {
        "target_service": "agent_service",
        "action": "query"
    })
    print(f"\nRouting Result: {result}")


def example_tts_bridge():
    """Example: Using the TTS Bridge."""
    print("\n" + "="*60)
    print("EXAMPLE 3: WSL-to-Windows TTS Bridge")
    print("="*60)
    
    bridge = TTSBridge()
    
    print(f"\nRunning in WSL: {bridge.is_wsl}")
    print(f"Available voices: {len(bridge.azure_client.voices)}")
    
    # List some voices
    voices = bridge.azure_client.list_voices()
    print("\nSample voices:")
    for i, (name, info) in enumerate(list(voices.items())[:3], 1):
        print(f"  {i}. {name} ({info['gender']}, {info['locale']})")
    
    # Generate SSML
    ssml = bridge.azure_client.generate_ssml(
        "Hello from the universal memory system!",
        voice="en-US-JennyNeural",
        rate="10%",
        pitch="5%"
    )
    print(f"\nGenerated SSML: {ssml[:100]}...")
    
    # Note: Actual TTS requires Azure credentials
    print("\n✓ TTS Bridge ready (set AZURE_TTS_KEY for full functionality)")


def example_ollama_manager():
    """Example: Using the Shared Ollama Instance."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Shared Ollama Instance (Singleton)")
    print("="*60)
    
    # Get the singleton instance
    ollama1 = OllamaManager()
    ollama2 = OllamaManager()
    
    # Verify singleton pattern
    print(f"\nSingleton verification: {ollama1 is ollama2}")
    
    # Check if Ollama is running
    print(f"Ollama running: {ollama1.is_running()}")
    
    if ollama1.is_running():
        # List models
        models = ollama1.list_models()
        print(f"Available models: {len(models)}")
        for model in models[:3]:
            print(f"  - {model.get('name', 'unknown')}")
        
        # Example generation (requires a model to be installed)
        # response = ollama1.generate("llama2", "Explain AI memory systems")
        # print(f"Response: {response[:100]}...")
    else:
        print("\n✓ Ollama Manager ready (start Ollama with 'ollama serve')")
    
    # Get status
    status = ollama1.get_status()
    print(f"\nOllama Status: {status}")


def example_universal_memory():
    """Example: Using Universal Memory directly."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Universal Memory - Context Liberation")
    print("="*60)
    
    from agents.memory import UniversalMemory, MemoryRetriever
    
    # Create memory system
    memory = UniversalMemory(storage_path=Path("example_memory.json"))
    retriever = MemoryRetriever(memory)
    
    print(f"\nInitial memories: {len(memory.memories)}")
    
    # Store various types of information
    print("\nStoring diverse memories...")
    
    memory.store(
        "Python is a high-level programming language.",
        importance=0.8,
        tags=["programming", "python"]
    )
    
    memory.store(
        "Machine learning is a subset of artificial intelligence.",
        importance=0.9,
        tags=["ai", "ml"]
    )
    
    memory.store(
        "The MCP architecture provides a single source of truth.",
        importance=1.0,
        tags=["architecture", "mcp"]
    )
    
    memory.store(
        "Universal memory systems enable context liberation.",
        importance=1.0,
        tags=["memory", "architecture"]
    )
    
    print(f"Total memories after storage: {len(memory.memories)}")
    
    # Search memories
    print("\n--- Searching for 'Python' ---")
    results = memory.search("Python", limit=3)
    for i, mem in enumerate(results, 1):
        print(f"  {i}. {mem.content}")
    
    print("\n--- Searching for 'architecture' ---")
    results = memory.search("architecture", limit=3)
    for i, mem in enumerate(results, 1):
        print(f"  {i}. {mem.content} (importance: {mem.importance})")
    
    # Search by tags
    print("\n--- Searching by tag 'ai' ---")
    results = memory.search_by_tags(["ai"], limit=3)
    for i, mem in enumerate(results, 1):
        print(f"  {i}. {mem.content}")
    
    # Get context
    print("\n--- Getting context for 'What is MCP?' ---")
    context = retriever.get_context("MCP", max_tokens=500)
    print(f"Context length: ~{len(context)//4} tokens")
    print(f"Context: {context[:150]}...")
    
    # Get statistics
    stats = memory.get_stats()
    print(f"\nMemory Statistics:")
    print(f"  Total Memories: {stats['total_memories']}")
    print(f"  Total Accesses: {stats['total_accesses']}")
    print(f"  Average Importance: {stats['average_importance']:.2f}")


def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("UNIVERSAL MEMORY SYSTEM - EXAMPLES")
    print("="*60)
    print("\nDemonstrating the MCP-first, model-agnostic architecture")
    print("that frees AI from context limits.\n")
    
    try:
        example_universal_memory()
        example_memory_agent()
        example_tts_bridge()
        example_ollama_manager()
        example_mcp_integration()
        
        print("\n" + "="*60)
        print("ALL EXAMPLES COMPLETED SUCCESSFULLY")
        print("="*60)
        print("\nKey Takeaways:")
        print("  ✓ Memory is model-agnostic - works with ANY AI")
        print("  ✓ MCP provides single source of truth")
        print("  ✓ Context is liberated from window limits")
        print("  ✓ All components integrate seamlessly")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
