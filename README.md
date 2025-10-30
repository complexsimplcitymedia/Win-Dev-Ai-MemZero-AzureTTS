# Win-Dev-Ai-MemZero-AzureTTS

## Universal, Model-Agnostic Memory System for AI

**Copilot Prime Directive**: This system creates a universal, model-agnostic memory, freeing AI from context limits. Architecture is MCP-first: The Master Control Program is the single source of truth for all gateways and services.

## Architecture Overview

This repository implements a **MCP-first (Master Control Program)** architecture that provides:

1. **Universal Memory System** - Model-agnostic memory that works with any AI model
2. **Context Liberation** - Frees AI from context window limitations
3. **Single Source of Truth** - MCP governs all gateways and services
4. **Critical Components**:
   - Python agent's memory/retrieval logic
   - WSL-to-Windows TTS bridge
   - Single, shared Ollama instance

## Key Components

### 1. MCP (Master Control Program)
**Location**: `mcp/core.py`

The Master Control Program is the **single source of truth** for all gateways and services. It:
- Manages service registry
- Routes requests through gateways
- Orchestrates all system components
- Maintains configuration state

```python
from mcp.core import MasterControlProgram

mcp = MasterControlProgram()
mcp.start()
```

### 2. Universal Memory System
**Location**: `agents/memory.py`

A **model-agnostic** memory system that:
- Stores memories independently of any specific AI model
- Provides intelligent retrieval
- Manages context to overcome context window limits
- Supports tagging, importance scoring, and search

```python
from agents.memory import UniversalMemory

memory = UniversalMemory()
memory_id = memory.store("Important information", importance=1.0)
results = memory.search("query", limit=10)
```

### 3. Memory Agent
**Location**: `agents/agent.py`

Python agent that integrates memory with any AI model:
- Model-agnostic conversation handling
- Automatic memory augmentation
- Context management
- MCP integration

```python
from agents.agent import MemoryAgent

agent = MemoryAgent("agent_id")
result = agent.process_input("User question", model_name="any-model")
agent.process_response("AI response", model_name="any-model")
```

### 4. WSL-to-Windows TTS Bridge
**Location**: `tts_bridge/bridge.py`

Bridges Linux WSL environment to Windows Azure TTS:
- Converts WSL paths to Windows paths
- Azure TTS integration
- SSML generation
- Audio playback across WSL boundary

```python
from tts_bridge.bridge import TTSBridge

bridge = TTSBridge()
bridge.speak("Hello from WSL!", voice="en-US-JennyNeural")
```

### 5. Shared Ollama Instance
**Location**: `ollama_config/manager.py`

**Single, shared Ollama instance** serving all AI models:
- Singleton pattern ensures one instance
- Model management (pull, load, list)
- Text generation and chat
- MCP integration

```python
from ollama_config.manager import OllamaManager

ollama = OllamaManager()  # Singleton - always returns same instance
ollama.start()
response = ollama.generate("llama2", "Your prompt here")
```

## Installation

### Prerequisites

- Python 3.8+
- Ollama (optional, for AI model inference)
- Azure Cognitive Services account (optional, for TTS)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/complexsimplcitymedia/Win-Dev-Ai-MemZero-AzureTTS.git
cd Win-Dev-Ai-MemZero-AzureTTS
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variables (optional):
```bash
export AZURE_TTS_KEY="your-azure-key"
export AZURE_TTS_REGION="eastus"
```

## Usage

### Quick Start

Run the main integration script to see the complete system in action:

```bash
python main.py
```

This will:
1. Initialize MCP (Master Control Program)
2. Set up the Universal Memory System
3. Configure the WSL-to-Windows TTS Bridge
4. Initialize the shared Ollama instance
5. Demonstrate memory storage and retrieval
6. Show model-agnostic conversation handling

### Using Individual Components

#### MCP - Master Control Program

```python
from mcp.core import MasterControlProgram, ServiceConfig, GatewayConfig

# Initialize MCP
mcp = MasterControlProgram()
mcp.start()

# Register a service
service = ServiceConfig(
    name="my_service",
    service_type="custom",
    endpoint="http://localhost:8000"
)
mcp.register_service(service)

# Register a gateway
gateway = GatewayConfig(
    name="my_gateway",
    gateway_type="router",
    target_services=["my_service"]
)
mcp.register_gateway(gateway)

# Route a request
result = mcp.route_request("my_gateway", {"target_service": "my_service"})
```

#### Memory Agent

```python
from agents.agent import MemoryAgent

# Create agent
agent = MemoryAgent("agent_1")

# Store memories
agent.remember("The sky is blue", importance=0.5, tags=["facts", "nature"])
agent.remember("Python is a programming language", importance=0.8, tags=["tech"])

# Recall memories
memories = agent.recall("Python", limit=5)

# Process conversation (model-agnostic)
result = agent.process_input("What is Python?", model_name="gpt-4")
agent.process_response("Python is a high-level programming language", model_name="gpt-4")

# Integrate with MCP
agent.integrate_with_mcp(mcp)
```

#### TTS Bridge

```python
from tts_bridge.bridge import TTSBridge

# Initialize bridge
bridge = TTSBridge()

# Convert text to speech
audio_file = bridge.speak(
    "Hello from the universal memory system!",
    voice="en-US-JennyNeural"
)

# Batch conversion
texts = ["First sentence", "Second sentence", "Third sentence"]
audio_files = bridge.batch_speak(texts)

# Integrate with MCP
bridge.integrate_with_mcp(mcp)
```

#### Ollama Manager

```python
from ollama_config.manager import OllamaManager

# Get singleton instance
ollama = OllamaManager()

# Start Ollama
ollama.start()

# List available models
models = ollama.list_models()

# Pull a model
ollama.pull_model("llama2")

# Generate text
response = ollama.generate("llama2", "Explain universal memory systems")

# Chat with conversation history
messages = [
    {"role": "user", "content": "Hello!"},
    {"role": "assistant", "content": "Hi there!"},
    {"role": "user", "content": "What is MCP?"}
]
response = ollama.chat("llama2", messages)

# Integrate with MCP
ollama.integrate_with_mcp(mcp)
```

## Architecture Principles

### 1. MCP-First Design
The Master Control Program is the **single source of truth**. All services register with MCP, and all routing goes through MCP gateways.

### 2. Model Agnostic
The memory system works with **any AI model** - GPT, Claude, Llama, Mistral, etc. No model-specific code in the core architecture.

### 3. Context Liberation
By providing persistent, searchable memory, the system **frees AI from context window limitations**. Long conversations and extensive knowledge bases are supported.

### 4. Singleton Ollama
A **single, shared Ollama instance** serves all AI models, ensuring efficient resource usage and consistent model management.

### 5. WSL Bridge
Seamlessly bridges Linux (WSL) and Windows environments for TTS capabilities, leveraging Azure Cognitive Services.

## Configuration

### MCP Configuration

Save and load MCP configuration:

```python
from pathlib import Path

# Save configuration
mcp.save_config(Path("mcp_config.json"))

# Load configuration
mcp.load_config(Path("mcp_config.json"))
```

### Memory Configuration

Configure memory storage location:

```python
from pathlib import Path
from agents.memory import UniversalMemory

memory = UniversalMemory(storage_path=Path("custom/path/memory.json"))
```

### Ollama Configuration

```python
from ollama_config.manager import OllamaConfig, OllamaManager

config = OllamaConfig(
    host="http://localhost:11434",
    keep_alive="10m"
)
ollama = OllamaManager(config)
```

## Directory Structure

```
Win-Dev-Ai-MemZero-AzureTTS/
├── mcp/                    # Master Control Program
│   ├── __init__.py
│   └── core.py            # MCP core implementation
├── agents/                 # Memory agents
│   ├── __init__.py
│   ├── memory.py          # Universal memory system
│   └── agent.py           # Memory agent
├── tts_bridge/            # WSL-to-Windows TTS bridge
│   ├── __init__.py
│   └── bridge.py          # TTS bridge implementation
├── ollama_config/         # Ollama management
│   ├── __init__.py
│   └── manager.py         # Shared Ollama instance
├── memory/                # Memory storage (created at runtime)
├── docs/                  # Documentation
├── main.py               # Main integration script
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Environment Variables

- `AZURE_TTS_KEY`: Azure Cognitive Services subscription key
- `AZURE_TTS_REGION`: Azure region (default: "eastus")

## Contributing

This is a living, breathing repository for open source collaboration. Contributions are welcome!

## License

Open Source - See LICENSE file for details.

## Governance

**This repository is governed by the Copilot Prime Directive**: Create a universal, model-agnostic memory system that frees AI from context limits. The MCP-first architecture must be maintained as the single source of truth for all gateways and services. The critical components (Python agent's memory/retrieval logic, WSL-to-Windows TTS bridge, and shared Ollama instance) are the foundation of this system.

---

**Note**: This system represents a paradigm shift in AI architecture, focusing on universal memory and model-agnostic design to truly free AI from limitations.
