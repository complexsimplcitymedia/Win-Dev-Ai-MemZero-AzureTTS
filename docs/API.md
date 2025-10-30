# API Reference

Complete API documentation for the Universal Memory System.

## MCP (Master Control Program)

### `MasterControlProgram`

Central orchestrator and single source of truth.

#### Constructor

```python
MasterControlProgram(config_path: Optional[Path] = None)
```

**Parameters:**
- `config_path`: Optional path to configuration file

#### Methods

##### `start()`
Start the MCP system.

```python
mcp.start()
```

##### `stop()`
Stop the MCP system.

```python
mcp.stop()
```

##### `register_service(service: ServiceConfig) -> bool`
Register a service with MCP.

```python
from mcp.core import ServiceConfig

service = ServiceConfig(
    name="my_service",
    service_type="custom",
    endpoint="http://localhost:8000",
    enabled=True,
    metadata={"key": "value"}
)
mcp.register_service(service)
```

##### `register_gateway(config: GatewayConfig) -> bool`
Register a gateway with MCP.

```python
from mcp.core import GatewayConfig

gateway = GatewayConfig(
    name="my_gateway",
    gateway_type="router",
    target_services=["service1", "service2"]
)
mcp.register_gateway(gateway)
```

##### `route_request(gateway_name: str, request: Dict[str, Any]) -> Dict[str, Any]`
Route a request through a gateway.

```python
result = mcp.route_request("my_gateway", {
    "target_service": "my_service",
    "action": "query"
})
```

##### `get_status() -> Dict[str, Any]`
Get current MCP status.

```python
status = mcp.get_status()
# Returns: {
#     "running": True,
#     "services": 3,
#     "gateways": 1,
#     "service_list": ["service1", "service2"],
#     "gateway_list": ["gateway1"]
# }
```

##### `save_config(path: Path)`
Save MCP configuration to file.

```python
mcp.save_config(Path("mcp_config.json"))
```

##### `load_config(path: Path)`
Load MCP configuration from file.

```python
mcp.load_config(Path("mcp_config.json"))
```

---

## Universal Memory System

### `UniversalMemory`

Model-agnostic persistent memory storage.

#### Constructor

```python
UniversalMemory(storage_path: Optional[Path] = None)
```

**Parameters:**
- `storage_path`: Path to memory storage file (default: "memory/universal_memory.json")

#### Methods

##### `store(content: str, metadata: Optional[Dict] = None, importance: float = 1.0, tags: Optional[List[str]] = None) -> str`
Store a new memory.

```python
memory_id = memory.store(
    content="Important information",
    metadata={"source": "user"},
    importance=0.9,
    tags=["important", "knowledge"]
)
```

**Returns:** Memory ID (string)

##### `retrieve(memory_id: str) -> Optional[MemoryEntry]`
Retrieve a specific memory by ID.

```python
entry = memory.retrieve(memory_id)
if entry:
    print(entry.content)
```

##### `search(query: str, limit: int = 10, min_importance: float = 0.0) -> List[MemoryEntry]`
Search memories by content.

```python
results = memory.search("Python", limit=5, min_importance=0.5)
for result in results:
    print(result.content)
```

##### `search_by_tags(tags: List[str], limit: int = 10) -> List[MemoryEntry]`
Search memories by tags.

```python
results = memory.search_by_tags(["ai", "ml"], limit=10)
```

##### `delete(memory_id: str) -> bool`
Delete a memory entry.

```python
success = memory.delete(memory_id)
```

##### `get_stats() -> Dict[str, Any]`
Get memory system statistics.

```python
stats = memory.get_stats()
# Returns: {
#     "total_memories": 100,
#     "total_accesses": 500,
#     "average_importance": 0.75,
#     "storage_path": "memory/universal_memory.json"
# }
```

##### `prune(max_age_seconds: Optional[float] = None, min_importance: Optional[float] = None, max_memories: Optional[int] = None)`
Prune old or low-importance memories.

```python
# Remove memories older than 30 days
memory.prune(max_age_seconds=30*24*60*60)

# Keep only top 1000 most important memories
memory.prune(max_memories=1000)

# Remove memories below importance threshold
memory.prune(min_importance=0.5)
```

### `MemoryRetriever`

Advanced memory retrieval system.

#### Constructor

```python
MemoryRetriever(universal_memory: UniversalMemory)
```

#### Methods

##### `get_context(query: str, max_tokens: int = 4000) -> str`
Retrieve relevant context for a query.

```python
context = retriever.get_context("What is MCP?", max_tokens=2000)
```

##### `get_recent_context(limit: int = 10) -> List[MemoryEntry]`
Get most recent memories.

```python
recent = retriever.get_recent_context(limit=5)
```

##### `get_important_context(limit: int = 10, min_importance: float = 0.5) -> List[MemoryEntry]`
Get most important memories.

```python
important = retriever.get_important_context(limit=10, min_importance=0.8)
```

---

## Memory Agent

### `MemoryAgent`

Model-agnostic AI agent with universal memory.

#### Constructor

```python
MemoryAgent(agent_id: str, memory_path: Optional[Path] = None)
```

**Parameters:**
- `agent_id`: Unique identifier for the agent
- `memory_path`: Optional custom memory storage path

#### Methods

##### `process_input(user_input: str, model_name: Optional[str] = None) -> Dict[str, Any]`
Process user input with memory augmentation.

```python
result = agent.process_input("What is Python?", model_name="gpt-4")
# Returns: {
#     "agent_id": "my_agent",
#     "input": "What is Python?",
#     "context": "...",
#     "memory_id": "abc123",
#     "model": "gpt-4"
# }
```

##### `process_response(response: str, model_name: Optional[str] = None) -> str`
Process and store AI response.

```python
memory_id = agent.process_response("Python is a language", model_name="gpt-4")
```

##### `remember(content: str, importance: float = 1.0, tags: Optional[List[str]] = None) -> str`
Store a memory with custom importance.

```python
memory_id = agent.remember(
    "Important fact",
    importance=0.9,
    tags=["fact", "important"]
)
```

##### `recall(query: str, limit: int = 10) -> List[str]`
Recall memories related to a query.

```python
memories = agent.recall("Python", limit=5)
```

##### `get_conversation_context(max_messages: int = 10) -> str`
Get recent conversation context.

```python
context = agent.get_conversation_context(max_messages=5)
```

##### `clear_conversation()`
Clear conversation history (keeps memories).

```python
agent.clear_conversation()
```

##### `get_stats() -> Dict[str, Any]`
Get agent statistics.

```python
stats = agent.get_stats()
```

##### `integrate_with_mcp(mcp_instance, service_name: Optional[str] = None)`
Integrate with MCP.

```python
agent.integrate_with_mcp(mcp, "my_agent_service")
```

---

## TTS Bridge

### `TTSBridge`

WSL-to-Windows TTS bridge for Azure TTS.

#### Constructor

```python
TTSBridge(azure_client: Optional[AzureTTSClient] = None)
```

#### Methods

##### `speak(text: str, voice: str = "en-US-JennyNeural", output_file: Optional[Path] = None, play_audio: bool = True) -> Optional[Path]`
Convert text to speech.

```python
audio_file = bridge.speak(
    "Hello world!",
    voice="en-US-JennyNeural",
    play_audio=True
)
```

**Available Voices:**
- `en-US-JennyNeural` (Female)
- `en-US-GuyNeural` (Male)
- `en-US-AriaNeural` (Female)
- `en-US-DavisNeural` (Male)
- `en-GB-SoniaNeural` (Female, British)
- `en-GB-RyanNeural` (Male, British)

##### `batch_speak(texts: List[str], voice: str = "en-US-JennyNeural", output_dir: Optional[Path] = None) -> List[Path]`
Convert multiple texts to speech.

```python
audio_files = bridge.batch_speak(
    ["First sentence", "Second sentence"],
    voice="en-US-JennyNeural"
)
```

##### `integrate_with_mcp(mcp_instance, service_name: str = "tts_bridge")`
Integrate with MCP.

```python
bridge.integrate_with_mcp(mcp)
```

### `AzureTTSClient`

Azure Text-to-Speech client.

#### Constructor

```python
AzureTTSClient(subscription_key: Optional[str] = None, region: Optional[str] = None)
```

**Parameters:**
- `subscription_key`: Azure subscription key (or set `AZURE_TTS_KEY` env var)
- `region`: Azure region (default: "eastus")

#### Methods

##### `generate_ssml(text: str, voice: str = "en-US-JennyNeural", rate: str = "0%", pitch: str = "0%") -> str`
Generate SSML for Azure TTS.

```python
ssml = client.generate_ssml(
    "Hello world",
    voice="en-US-JennyNeural",
    rate="10%",  # -100% to +200%
    pitch="5%"   # -50% to +50%
)
```

##### `list_voices() -> Dict[str, Dict[str, str]]`
List available voices.

```python
voices = client.list_voices()
```

---

## Ollama Manager

### `OllamaManager`

Single shared Ollama instance (singleton).

#### Constructor

```python
OllamaManager(config: Optional[OllamaConfig] = None)
```

**Note:** Always returns the same instance (singleton pattern).

#### Methods

##### `start() -> bool`
Start Ollama service.

```python
success = ollama.start()
```

##### `stop() -> bool`
Stop Ollama service.

```python
ollama.stop()
```

##### `is_running() -> bool`
Check if Ollama is running.

```python
if ollama.is_running():
    print("Ollama is ready")
```

##### `list_models() -> List[Dict[str, Any]]`
List available models.

```python
models = ollama.list_models()
for model in models:
    print(model['name'])
```

##### `pull_model(model_name: str) -> bool`
Pull/download a model.

```python
success = ollama.pull_model("llama2")
```

##### `load_model(model_name: str) -> bool`
Load a model into memory.

```python
ollama.load_model("llama2")
```

##### `generate(model_name: str, prompt: str, stream: bool = False, **kwargs) -> Optional[str]`
Generate text using a model.

```python
response = ollama.generate(
    "llama2",
    "Explain AI memory systems",
    stream=False,
    temperature=0.7
)
```

##### `chat(model_name: str, messages: List[Dict[str, str]], stream: bool = False, **kwargs) -> Optional[str]`
Chat with a model.

```python
response = ollama.chat("llama2", [
    {"role": "user", "content": "Hello!"},
    {"role": "assistant", "content": "Hi!"},
    {"role": "user", "content": "What is MCP?"}
])
```

##### `get_status() -> Dict[str, Any]`
Get Ollama status.

```python
status = ollama.get_status()
```

##### `integrate_with_mcp(mcp_instance, service_name: str = "ollama_shared")`
Integrate with MCP.

```python
ollama.integrate_with_mcp(mcp)
```

---

## Data Structures

### `ServiceConfig`

```python
@dataclass
class ServiceConfig:
    name: str
    service_type: str
    endpoint: str
    enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)
```

### `GatewayConfig`

```python
@dataclass
class GatewayConfig:
    name: str
    gateway_type: str
    target_services: List[str] = field(default_factory=list)
    enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)
```

### `MemoryEntry`

```python
@dataclass
class MemoryEntry:
    id: str
    content: str
    timestamp: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    embedding: Optional[List[float]] = None
    importance: float = 1.0
    access_count: int = 0
    last_accessed: float = field(default_factory=time.time)
    tags: List[str] = field(default_factory=list)
```

---

## Environment Variables

- `AZURE_TTS_KEY`: Azure Cognitive Services subscription key
- `AZURE_TTS_REGION`: Azure region (default: "eastus")
- `OLLAMA_HOST`: Ollama host URL (default: "http://localhost:11434")
- `OLLAMA_KEEP_ALIVE`: Keep-alive duration (default: "5m")
- `MEMORY_STORAGE_PATH`: Custom memory storage path
- `MCP_CONFIG_PATH`: Custom MCP configuration path
- `LOG_LEVEL`: Logging level (default: "INFO")

---

## Error Handling

All methods that can fail return appropriate error indicators:
- Boolean methods return `False` on failure
- Methods returning objects return `None` on failure
- Methods returning collections return empty collections on failure

Always check return values:

```python
if not ollama.start():
    print("Failed to start Ollama")

result = memory.retrieve(memory_id)
if result is None:
    print("Memory not found")
```

---

## Thread Safety

All core components are thread-safe:
- `MasterControlProgram`: Uses locks for service/gateway operations
- `UniversalMemory`: Thread-safe storage and retrieval
- `MemoryAgent`: Safe for concurrent access
- `OllamaManager`: Singleton with thread-safe operations

---

For more information, see the [Architecture Documentation](ARCHITECTURE.md) and [Quick Start Guide](QUICKSTART.md).
