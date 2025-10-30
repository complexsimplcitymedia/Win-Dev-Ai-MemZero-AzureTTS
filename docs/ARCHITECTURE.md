# Architecture Documentation

## MCP-First Universal Memory System

### Overview

This system implements a revolutionary approach to AI memory management through a **MCP-first (Master Control Program)** architecture. The key innovation is creating a **universal, model-agnostic memory** that frees AI from context limitations.

## Core Architectural Principles

### 1. Single Source of Truth
The Master Control Program (MCP) serves as the central authority for:
- Service registration and discovery
- Gateway routing and orchestration
- Configuration management
- System-wide coordination

### 2. Model Agnosticism
The memory system is completely independent of any specific AI model:
- Works with GPT, Claude, Llama, Mistral, etc.
- No model-specific APIs or dependencies in core code
- Universal memory format that any model can consume

### 3. Context Liberation
By providing persistent, searchable memory outside the model's context window:
- Conversations can extend indefinitely
- Knowledge accumulates over time
- Context is retrieved on-demand, not stored in-window
- Effectively unlimited memory capacity

## System Components

### MCP (Master Control Program)

**Purpose**: Central orchestrator and single source of truth

**Key Features**:
- Service Registry: Maintains catalog of all services
- Gateway Management: Routes requests to appropriate services
- Configuration Persistence: Saves/loads system state
- Thread-safe operations

**Design Pattern**: Centralized coordinator with distributed services

### Universal Memory System

**Purpose**: Model-agnostic persistent memory storage

**Key Features**:
- Memory Entries: Content + metadata + importance + tags
- Search Capabilities: Text-based and tag-based search
- Access Tracking: Monitors memory usage patterns
- Pruning: Automatic cleanup of old/unimportant memories

**Design Pattern**: Repository pattern with intelligent retrieval

### Memory Agent

**Purpose**: Bridge between AI models and universal memory

**Key Features**:
- Model-Agnostic Processing: Works with any AI model
- Context Augmentation: Enriches queries with relevant memories
- Conversation Tracking: Maintains dialogue history
- MCP Integration: Registers as a service

**Design Pattern**: Agent pattern with memory augmentation

### WSL-to-Windows TTS Bridge

**Purpose**: Enable Azure TTS from Linux/WSL environments

**Key Features**:
- Path Translation: WSL ↔ Windows path conversion
- Azure TTS Client: Generates SSML and calls Azure services
- Audio Playback: Plays audio on Windows from WSL
- Batch Processing: Multiple text-to-speech conversions

**Design Pattern**: Bridge pattern for cross-platform integration

### Shared Ollama Instance

**Purpose**: Single AI model backend for the entire system

**Key Features**:
- Singleton Pattern: Ensures only one instance
- Model Management: Pull, load, and manage models
- Text Generation: Standard generation API
- Chat Interface: Conversation-based interaction

**Design Pattern**: Singleton for resource management

## Data Flow

### Memory Storage Flow
```
User Input → Memory Agent → Universal Memory → Persistent Storage
```

### Memory Retrieval Flow
```
Query → Memory Retriever → Search Memory → Ranked Results → Context Assembly
```

### MCP Request Routing Flow
```
Client → Gateway → MCP Router → Service Registry → Target Service
```

### TTS Flow (WSL)
```
Text → TTS Bridge → Path Translation → Azure TTS → Windows Audio Playback
```

## Thread Safety

All core components implement thread-safe operations:
- `threading.Lock()` for critical sections
- Atomic operations where possible
- Safe concurrent access to shared resources

## Persistence

### Memory Persistence
- Format: JSON
- Location: Configurable (default: `memory/universal_memory.json`)
- Auto-save: After every memory operation

### MCP Configuration Persistence
- Format: JSON
- Location: Configurable (default: `mcp_config.json`)
- Manual save/load: Via API calls

## Scalability Considerations

### Memory Scalability
- Pruning mechanisms prevent unbounded growth
- Importance-based retention
- Age-based cleanup
- Size-based limits

### Service Scalability
- MCP can manage unlimited services
- Services can be distributed across processes/machines
- Gateway routing supports load balancing patterns

## Security Considerations

### Memory Security
- Local storage by default
- No external transmission unless explicitly configured
- Metadata can include access control information

### TTS Security
- Azure credentials via environment variables
- No hardcoded secrets
- Secure credential management recommended

## Extension Points

### Custom Services
Register any service with MCP:
```python
service = ServiceConfig(
    name="custom_service",
    service_type="custom",
    endpoint="http://localhost:8000"
)
mcp.register_service(service)
```

### Custom Gateways
Create specialized routing logic:
```python
gateway = GatewayConfig(
    name="custom_gateway",
    gateway_type="specialized",
    target_services=["service1", "service2"]
)
mcp.register_gateway(gateway)
```

### Custom Memory Backends
Extend `UniversalMemory` to use different storage:
- Database backends (PostgreSQL, MongoDB)
- Vector databases (Pinecone, Weaviate)
- Cloud storage (S3, Azure Blob)

## Future Enhancements

### Planned Features
1. **Semantic Search**: Vector embeddings for better retrieval
2. **Distributed Memory**: Multi-node memory sharing
3. **Memory Sync**: Cross-instance synchronization
4. **Advanced Pruning**: ML-based importance scoring
5. **Real-time TTS**: Streaming Azure TTS
6. **Multi-model Ollama**: Automatic model selection

### Integration Opportunities
- LangChain integration
- LlamaIndex compatibility
- OpenAI API compatibility layer
- Anthropic Claude integration
- Custom model adapters

## Performance Characteristics

### Memory Operations
- Store: O(1)
- Retrieve by ID: O(1)
- Search: O(n) where n = total memories
- Prune: O(n)

### MCP Operations
- Service lookup: O(1) (dictionary)
- Gateway routing: O(1)
- Configuration save/load: O(s) where s = number of services

## Testing Strategy

### Unit Tests
- Test each component in isolation
- Mock external dependencies
- Validate thread safety

### Integration Tests
- Test component interactions
- Verify MCP orchestration
- Validate memory persistence

### System Tests
- End-to-end scenarios
- Performance benchmarks
- Stress testing

## Monitoring and Observability

### Built-in Statistics
- Memory stats: `memory.get_stats()`
- Agent stats: `agent.get_stats()`
- MCP status: `mcp.get_status()`
- Ollama status: `ollama.get_status()`

### Logging
- Structured logging throughout
- Configurable log levels
- Component-specific loggers

## Deployment Patterns

### Single Machine
All components run on one machine - suitable for development and small deployments.

### Distributed
MCP and services can run on separate machines, communicating via network.

### Containerized
Each component can run in its own container, orchestrated by Kubernetes or Docker Compose.

## Governance Model

This architecture is governed by the **Copilot Prime Directive**:
- MCP remains the single source of truth
- Memory must remain model-agnostic
- Critical components must not be compromised
- Architecture decisions prioritize universality over optimization

---

*This documentation is living and should be updated as the architecture evolves.*
