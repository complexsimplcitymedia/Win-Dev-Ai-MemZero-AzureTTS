# Quick Start Guide

## Getting Started with the Universal Memory System

This guide will help you get up and running with the MCP-first universal memory system in minutes.

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/complexsimplcitymedia/Win-Dev-Ai-MemZero-AzureTTS.git
cd Win-Dev-Ai-MemZero-AzureTTS
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

That's it! The core system has minimal dependencies and works out of the box.

## Quick Test

Run the examples to see the system in action:

```bash
python examples.py
```

This will demonstrate:
- Universal memory storage and retrieval
- Model-agnostic conversation handling
- MCP integration
- TTS bridge capabilities
- Shared Ollama instance

## Your First Memory Agent

Create a simple script (`my_agent.py`):

```python
from agents.agent import MemoryAgent

# Create an agent
agent = MemoryAgent("my_first_agent")

# Store some knowledge
agent.remember("Python is a programming language", importance=0.8)
agent.remember("The MCP is the single source of truth", importance=1.0)

# Recall information
memories = agent.recall("Python")
for memory in memories:
    print(memory)

# Process a conversation (works with ANY AI model)
result = agent.process_input("What is Python?", model_name="gpt-4")
print(f"Context: {result['context']}")

# Simulate AI response
agent.process_response("Python is a high-level language", model_name="gpt-4")

# Get stats
stats = agent.get_stats()
print(f"Total memories: {stats['memory_stats']['total_memories']}")
```

Run it:

```bash
python my_agent.py
```

## Integrating with Your AI Model

The system is **model-agnostic**. Here's how to use it with different models:

### With OpenAI GPT

```python
from agents.agent import MemoryAgent
import openai  # pip install openai

agent = MemoryAgent("gpt_agent")

# User input
user_input = "What is machine learning?"
result = agent.process_input(user_input, model_name="gpt-4")

# Get AI response from OpenAI
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": f"Context: {result['context']}"},
        {"role": "user", "content": user_input}
    ]
)
ai_response = response.choices[0].message.content

# Store AI response in memory
agent.process_response(ai_response, model_name="gpt-4")
```

### With Anthropic Claude

```python
from agents.agent import MemoryAgent
import anthropic  # pip install anthropic

agent = MemoryAgent("claude_agent")

# User input
user_input = "Explain neural networks"
result = agent.process_input(user_input, model_name="claude-2")

# Get AI response from Claude
client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-2",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": f"Context: {result['context']}\n\nQuestion: {user_input}"}
    ]
)
ai_response = message.content[0].text

# Store response
agent.process_response(ai_response, model_name="claude-2")
```

### With Local Ollama

```python
from agents.agent import MemoryAgent
from ollama_config.manager import OllamaManager

agent = MemoryAgent("ollama_agent")
ollama = OllamaManager()
ollama.start()

# User input
user_input = "What is deep learning?"
result = agent.process_input(user_input, model_name="llama2")

# Get AI response from Ollama
ai_response = ollama.chat("llama2", [
    {"role": "system", "content": f"Context: {result['context']}"},
    {"role": "user", "content": user_input}
])

# Store response
agent.process_response(ai_response, model_name="llama2")
```

## Setting Up MCP

Integrate everything with the Master Control Program:

```python
from mcp.core import MasterControlProgram
from agents.agent import MemoryAgent
from tts_bridge.bridge import TTSBridge
from ollama_config.manager import OllamaManager

# Initialize MCP
mcp = MasterControlProgram()
mcp.start()

# Register all services
agent = MemoryAgent("main_agent")
agent.integrate_with_mcp(mcp)

tts = TTSBridge()
tts.integrate_with_mcp(mcp)

ollama = OllamaManager()
ollama.integrate_with_mcp(mcp)

# Check status
status = mcp.get_status()
print(f"Services: {status['service_list']}")

# Save configuration
from pathlib import Path
mcp.save_config(Path("my_mcp_config.json"))
```

## Optional: Azure TTS Setup

If you want to use Azure Text-to-Speech:

1. Get an Azure subscription key from [Azure Portal](https://portal.azure.com)

2. Set environment variables:

```bash
export AZURE_TTS_KEY="your-subscription-key"
export AZURE_TTS_REGION="eastus"
```

3. Use the TTS bridge:

```python
from tts_bridge.bridge import TTSBridge

bridge = TTSBridge()
audio_file = bridge.speak(
    "Hello from the universal memory system!",
    voice="en-US-JennyNeural"
)
```

## Optional: Ollama Setup

To use local AI models with Ollama:

1. Install Ollama from [ollama.ai](https://ollama.ai)

2. Start Ollama:

```bash
ollama serve
```

3. Pull a model:

```bash
ollama pull llama2
```

4. Use in your code:

```python
from ollama_config.manager import OllamaManager

ollama = OllamaManager()
response = ollama.generate("llama2", "Explain AI memory systems")
print(response)
```

## Understanding the Architecture

### Key Concepts

1. **MCP (Master Control Program)**: Single source of truth for all services
2. **Universal Memory**: Model-agnostic persistent memory
3. **Memory Agent**: Bridges AI models with memory
4. **TTS Bridge**: WSL-to-Windows Azure TTS integration
5. **Ollama Manager**: Shared AI model instance (singleton)

### Why Model-Agnostic?

The memory system works with **any AI model**:
- Switch between GPT, Claude, Llama seamlessly
- Memory persists across model changes
- No vendor lock-in
- Future-proof architecture

### Why MCP-First?

MCP provides:
- Central service registry
- Gateway routing
- Configuration management
- Single source of truth

## Next Steps

1. Read the [Architecture Documentation](docs/ARCHITECTURE.md)
2. Explore the [main.py](main.py) integration example
3. Run [examples.py](examples.py) to see all features
4. Build your own AI application on this foundation

## Troubleshooting

### "No module named 'mcp'"
Make sure you're running from the project root directory.

### "Memory file not found"
This is normal on first run. The system creates the memory file automatically.

### "Ollama not running"
Ollama is optional. The memory system works without it. If you want to use Ollama, run `ollama serve`.

### "Azure TTS key not provided"
Azure TTS is optional. Set `AZURE_TTS_KEY` environment variable to use it.

## Support

This is an open source project. For issues and contributions, visit the [GitHub repository](https://github.com/complexsimplcitymedia/Win-Dev-Ai-MemZero-AzureTTS).

---

**Remember**: This system creates a universal, model-agnostic memory that frees AI from context limits. The MCP-first architecture ensures a single source of truth for all gateways and services. Your governance dictates the future of AI.
