# Windows AI Assistant - Complete Local AI Platform

**The Complete Local AI Stack** - CPU + GPU + Memory + Voice + MCP Servers

All running 100% local on Windows, WSL, and Tailscale network. No cloud dependencies.

## 🎯 What We Added

### ✅ TTS Server (Text-to-Speech)
- **Service:** Azure Cognitive Speech Services
- **Location:** `services/azure-tts/`
- **Purpose:** All AI responses are spoken via neural voices
- **Status:** Production-ready MCP server

### ✅ mem0 Local Memory Server
- **Service:** Persistent memory and learning system
- **Location:** `services/memory/` (WSL)
- **API:** REST endpoints at `http://localhost:8765`
- **Features:**
  - Automatic fact extraction from conversations
  - Keyword-based memory search
  - Persistent JSON storage
  - Real-time memory tracking
- **Status:** Production-ready

### ✅ MCP Server Hub (Model Context Protocol)
- **Location:** `src/mcp_servers/orchestrator/`
- **Purpose:** Central hub connecting 11+ MCP servers
- **Servers Available:**
  - 🎙️ Azure TTS (voice output)
  - 📚 Context7 (documentation access)
  - 🔍 Brave Search (web search)
  - 🌐 Firecrawl (web scraping)
  - 💼 GitHub (repository management)
  - 💼 Bright Data (job site scraping)
  - 🔎 DuckDuckGo (lightweight search)
  - 🤖 Nebius (AI inference)
  - 🎭 Playwright (browser automation)
  - ⚙️ Zapier (workflow automation)
  - 🎯 Job Hunt (job aggregation)

## 📺 Video Tutorial

**Getting Started Guide:** [Watch on YouTube](https://www.youtube.com/watch?v=rl5u9Yb2Ir4&t=3046s)

---

## 🏗️ Architecture

```
windows-ai-assistant/               (ROOT - Main orchestrator)
├── src/                            (Core system)
│   ├── core/                       # Assistant orchestrator
│   ├── ai/                         # Ollama integration (GPU)
│   ├── control/                    # Device control
│   ├── speech/                     # Speech recognition
│   ├── config/                     # Settings
│   └── mcp_servers/orchestrator/   # MCP hub (11+ servers)
│
├── services/                       (Modular services)
│   ├── azure-tts/                  # Text-to-Speech Service ✨ NEW
│   │   ├── mcp_tts_server.py      # MCP interface
│   │   ├── engine.py              # Azure TTS engine
│   │   ├── docker/                # Containerization
│   │   └── README_MCP.md          # Setup guide
│   │
│   └── memory/                     # mem0 Memory Service ✨ NEW
│       ├── mem0_client.py         # Memory integration
│       ├── REST API               # Memory endpoints
│       └── Persistent storage     # Local JSON DB
│
├── main.py                         (Entry point)
├── requirements.txt                (Core: Ollama, PyWin32, etc)
├── requirements_azure_tts.txt      (TTS: Azure SDK, MCP)
├── requirements_memory.txt         (Memory: mem0, REST client)
└── README.md
```

---

## 🚀 Quick Start

### Install Core

```bash
pip install -r requirements.txt
```

### Install All Services (Optional)

```bash
pip install -r requirements_azure_tts.txt
pip install -r requirements_memory.txt
```

### Run Main Assistant

```bash
python main.py
```

### Run Individual Services

```bash
# Run Azure TTS service
python services/azure-tts/run_service.py

# Run Memory service
python services/memory/run_service.py
```

---

## 📦 Services

### Azure TTS
- **Path:** `services/azure-tts/`
- **Purpose:** Text-to-speech via Azure or fallback to native OS
- **Entry:** `python services/azure-tts/run_service.py`
- **Dependencies:** `requirements_azure_tts.txt`

### Memory
- **Path:** `services/memory/`
- **Purpose:** Persistent learning and memory via mem0
- **Entry:** `python services/memory/run_service.py`
- **Dependencies:** `requirements_memory.txt`

---

## 🔧 Development

Each service:
- Has its own source code in `services/SERVICE_NAME/`
- Has its own entry point: `run_service.py`
- Has its own requirements file: `requirements_SERVICE_NAME.txt`
- Can be developed/tested independently
- Integrates via MCP or REST APIs

### Adding a New Service

1. Create directory: `services/my_service/`
2. Create entry point: `services/my_service/run_service.py`
3. Create requirements: `requirements_my_service.txt`
4. Update this README with service documentation

---

## 🔌 Integration

Services communicate via:
- **MCP Protocol** - Azure TTS (Model Context Protocol)
- **REST APIs** - Memory service
- **Environment variables** - Configuration

See `src/core/assistant.py` for orchestration.

---

## 📝 Configuration

1. Copy `.env.example` to `.env`
2. Add your Azure Speech Services keys
3. Add your mem0 API key
4. Start main assistant: `python main.py`

---

## 🐳 Docker (Optional)

Each service has optional Docker support:

```bash
docker build -f services/azure-tts/docker/Dockerfile -t azure-tts .
docker run -e AZURE_SPEECH_KEY=... azure-tts
```

---

## 📚 Documentation

- [QUICKSTART_TTS.md](S:\mem0\QUICKSTART_TTS.md) - Quick TTS setup
- [TTS_INTEGRATION_GUIDE.md](S:\mem0\TTS_INTEGRATION_GUIDE.md) - Full TTS integration
- [INTEGRATION_SUMMARY.md](S:\mem0\INTEGRATION_SUMMARY.md) - Detailed changes
- [MCP_INTEGRATION_GUIDE.md](MCP_INTEGRATION_GUIDE.md) - MCP server integration
- [MONOREPO_ORGANIZATION_GUIDE.md](MONOREPO_ORGANIZATION_GUIDE.md) - Monorepo structure

---

## 🎯 Features

✅ **100% Local Processing**
- Ollama GPU inference on Windows
- All data stays on your machine
- No cloud dependencies

✅ **Voice Integration**
- Azure TTS text-to-speech
- Agent speaks all responses
- Optional voice toggle

✅ **Persistent Memory**
- Local JSON-based storage
- Learns from conversations
- Fact extraction and retrieval

✅ **Modular Architecture**
- Independent services
- Easy to add new services
- Clear separation of concerns

---

## 🔐 Privacy

- ✅ 100% local processing
- ✅ No external API calls (except optional Azure for TTS)
- ✅ All data stored locally
- ✅ Full control over your data
- ✅ No telemetry
- ✅ No tracking

---

## 🎉 License

MIT License - See LICENSE file

---

**All services run locally. Everything stays private. All yours.**

**[Watch the setup video →](https://www.youtube.com/watch?v=rl5u9Yb2Ir4&t=3046s)**

