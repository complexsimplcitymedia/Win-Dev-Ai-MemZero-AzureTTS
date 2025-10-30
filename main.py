"""
Main Integration Script
Demonstrates the complete MCP-first architecture with all components.
"""

import logging
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from mcp.core import MasterControlProgram, GatewayConfig
from agents.agent import MemoryAgent
from tts_bridge.bridge import TTSBridge
from ollama_config.manager import OllamaManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    """
    Main entry point demonstrating the universal memory system.
    This system creates a model-agnostic memory that frees AI from context limits.
    Architecture is MCP-first: The Master Control Program is the single source of truth.
    """
    
    logger.info("=" * 80)
    logger.info("INITIALIZING UNIVERSAL MEMORY SYSTEM")
    logger.info("MCP-First Architecture - Model Agnostic AI Memory")
    logger.info("=" * 80)
    
    # 1. Initialize MCP (Master Control Program) - Single Source of Truth
    logger.info("\n[1/4] Initializing Master Control Program (MCP)...")
    mcp = MasterControlProgram()
    mcp.start()
    
    # 2. Initialize Memory Agent with Universal Memory
    logger.info("\n[2/4] Initializing Memory Agent with Universal Memory...")
    memory_agent = MemoryAgent(
        agent_id="primary_agent",
        memory_path=Path("memory/universal_memory.json")
    )
    memory_agent.integrate_with_mcp(mcp, "primary_memory_agent")
    
    # 3. Initialize WSL-to-Windows TTS Bridge
    logger.info("\n[3/4] Initializing WSL-to-Windows TTS Bridge...")
    tts_bridge = TTSBridge()
    tts_bridge.integrate_with_mcp(mcp, "azure_tts_bridge")
    
    # 4. Initialize Single Shared Ollama Instance
    logger.info("\n[4/4] Initializing Shared Ollama Instance...")
    ollama = OllamaManager()
    ollama.integrate_with_mcp(mcp, "ollama_shared")
    
    # Configure Gateway for routing
    logger.info("\nConfiguring MCP Gateway...")
    gateway_config = GatewayConfig(
        name="main_gateway",
        gateway_type="universal",
        target_services=["primary_memory_agent", "azure_tts_bridge", "ollama_shared"],
        enabled=True,
        metadata={"role": "primary_router"}
    )
    mcp.register_gateway(gateway_config)
    
    # Display System Status
    logger.info("\n" + "=" * 80)
    logger.info("SYSTEM STATUS")
    logger.info("=" * 80)
    
    mcp_status = mcp.get_status()
    logger.info(f"\nMCP Status:")
    logger.info(f"  Running: {mcp_status['running']}")
    logger.info(f"  Services: {mcp_status['services']}")
    logger.info(f"  Gateways: {mcp_status['gateways']}")
    logger.info(f"  Registered Services: {', '.join(mcp_status['service_list'])}")
    
    agent_stats = memory_agent.get_stats()
    logger.info(f"\nMemory Agent Status:")
    logger.info(f"  Agent ID: {agent_stats['agent_id']}")
    logger.info(f"  Total Memories: {agent_stats['memory_stats']['total_memories']}")
    logger.info(f"  Storage: {agent_stats['memory_stats']['storage_path']}")
    
    ollama_status = ollama.get_status()
    logger.info(f"\nOllama Status:")
    logger.info(f"  Running: {ollama_status['running']}")
    logger.info(f"  Host: {ollama_status['host']}")
    logger.info(f"  Available Models: {ollama_status['available_models']}")
    
    # Demonstrate Memory System
    logger.info("\n" + "=" * 80)
    logger.info("DEMONSTRATING UNIVERSAL MEMORY SYSTEM")
    logger.info("=" * 80)
    
    # Store some memories
    logger.info("\nStoring memories in universal memory system...")
    memory_agent.remember(
        "The MCP (Master Control Program) is the single source of truth for all gateways and services.",
        importance=1.0,
        tags=["architecture", "mcp", "core"]
    )
    
    memory_agent.remember(
        "The universal memory system is model-agnostic and frees AI from context limits.",
        importance=1.0,
        tags=["memory", "architecture", "core"]
    )
    
    memory_agent.remember(
        "The WSL-to-Windows TTS bridge enables Azure TTS from Linux environments.",
        importance=0.9,
        tags=["tts", "bridge", "azure"]
    )
    
    memory_agent.remember(
        "A single, shared Ollama instance serves all AI models in the system.",
        importance=0.9,
        tags=["ollama", "ai-models", "shared"]
    )
    
    # Retrieve memories
    logger.info("\nRetrieving memories about 'MCP'...")
    mcp_memories = memory_agent.recall("MCP", limit=5)
    for i, memory in enumerate(mcp_memories, 1):
        logger.info(f"  {i}. {memory}")
    
    logger.info("\nRetrieving memories about 'memory system'...")
    memory_memories = memory_agent.recall("memory system", limit=5)
    for i, memory in enumerate(memory_memories, 1):
        logger.info(f"  {i}. {memory}")
    
    # Demonstrate conversation with memory augmentation
    logger.info("\n" + "=" * 80)
    logger.info("DEMONSTRATING CONVERSATION WITH MEMORY AUGMENTATION")
    logger.info("=" * 80)
    
    user_input = "What is the Master Control Program?"
    logger.info(f"\nUser Input: {user_input}")
    
    result = memory_agent.process_input(user_input, model_name="any-ai-model")
    logger.info(f"\nContext Retrieved (model-agnostic):")
    if result['context']:
        logger.info(f"  {result['context'][:200]}...")
    else:
        logger.info("  (No prior context found)")
    
    # Simulate AI response
    ai_response = "The Master Control Program (MCP) is the single source of truth for all gateways and services in this architecture."
    memory_agent.process_response(ai_response, model_name="any-ai-model")
    logger.info(f"\nAI Response stored in memory: {ai_response}")
    
    # Save MCP configuration
    logger.info("\n" + "=" * 80)
    logger.info("SAVING CONFIGURATION")
    logger.info("=" * 80)
    
    config_path = Path("mcp_config.json")
    mcp.save_config(config_path)
    logger.info(f"\nMCP configuration saved to: {config_path}")
    
    logger.info("\n" + "=" * 80)
    logger.info("SYSTEM INITIALIZATION COMPLETE")
    logger.info("Universal Memory System is operational")
    logger.info("MCP-First Architecture established")
    logger.info("=" * 80)
    
    return mcp, memory_agent, tts_bridge, ollama


if __name__ == "__main__":
    mcp, memory_agent, tts_bridge, ollama = main()
    
    print("\n" + "=" * 80)
    print("INTERACTIVE MODE")
    print("=" * 80)
    print("\nThe system is now running. You can:")
    print("  - Query the memory agent: memory_agent.recall('query')")
    print("  - Store new memories: memory_agent.remember('content', importance=1.0)")
    print("  - Check MCP status: mcp.get_status()")
    print("  - Access TTS bridge: tts_bridge.speak('text')")
    print("  - Access Ollama: ollama.get_status()")
    print("\nPress Ctrl+C to exit.")
    print("=" * 80)
    
    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nShutting down...")
        mcp.stop()
        print("System shutdown complete.")
