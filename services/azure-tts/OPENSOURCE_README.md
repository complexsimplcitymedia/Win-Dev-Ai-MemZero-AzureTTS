# Universal AI Text-to-Speech System

> **Hybrid TTS Server with MCP Protocol & REST API**
>
> Provides universal text-to-speech capabilities across multiple AI models (Claude, Ollama, Gemini, etc.) via MCP (Model Context Protocol) and REST API, with support for Bluetooth audio on WSL.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Azure TTS](https://img.shields.io/badge/Azure-Cognitive_Services-blue)](https://azure.microsoft.com/en-us/services/cognitive-services/text-to-speech/)

## 🎯 Features

- **🔌 Dual Protocol Support**: MCP (STDIO) for AI model integration + REST API for general use
- **🎤 Azure Neural Voices**: High-quality text-to-speech with multiple voice options
- **🔊 Bluetooth Audio**: Full support for Bluetooth audio devices on WSL via Windows
- **🌐 Universal Compatibility**: Works with any MCP-compatible AI client
- **⚡ Low Latency**: Direct process communication via STDIO (no HTTP overhead for MCP)
- **🛠️ Production Ready**: Both development Flask server and production-ready architecture

## 📋 Table of Contents

- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Integration Examples](#integration-examples)
- [API Reference](#api-reference)
- [Contributing](#contributing)

## 🏗️ Architecture

### System Overview

```
┌─────────────────────────────────────────────────────┐
│        AI Models (Claude/Ollama/Gemini/etc)         │
└──────────────────┬──────────────┬───────────────────┘
                   │              │
           ┌───────▼─────┐   ┌────▼────────┐
           │   MCP Mode  │   │  REST API   │
           │   (STDIO)   │   │   (Flask)   │
           └───────┬─────┘   └────┬────────┘
                   │              │
           ┌───────▼──────────────▼─────────┐
           │   Hybrid TTS Server            │
           │   (simple_hybrid_server.py)    │
           └───────┬────────────────────────┘
                   │
           ┌───────▼────────┐
           │  Azure Speech  │
           │  SDK (Neural)  │
           └───────┬────────┘
                   │
           ┌───────▼────────┐
           │  Audio Output  │
           │  - Bluetooth   │
           │  - Speakers    │
           │  - File        │
           └────────────────┘
```

### Why Hybrid Architecture?

**MCP (STDIO) Mode:**
- ✅ No network timeouts
- ✅ Direct process communication
- ✅ Standard protocol for AI tools
- ✅ Works with any MCP-compatible client

**REST API (Flask) Mode:**
- ✅ Easy testing and debugging
- ✅ Works with any HTTP client
- ✅ Simple integration for non-MCP clients
- ✅ Browser/web application support

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Azure Cognitive Services Speech API key ([Get one free](https://azure.microsoft.com/en-us/services/cognitive-services/text-to-speech/))
- WSL2 (if on Windows) or Linux/macOS
- For Bluetooth: Windows with Bluetooth device paired

### 1. Clone and Install

```bash
cd azure_tts
pip install -r requirements_mcp.txt
```

### 2. Configure Azure Credentials

Create `.env` file:

```bash
cp .env.example .env
# Edit .env with your Azure credentials
```

```.env
# Azure Speech Service Credentials
AZURE_SPEECH_KEY=your_azure_key_here
AZURE_SPEECH_REGION=eastus

# Voice Settings (optional)
VOICE_NAME=en-US-GuyNeural
VOICE_RATE=+0%
VOICE_PITCH=+0Hz
```

### 3. Test It

```bash
# Test Bluetooth TTS
python3 speak_bluetooth.py "Hello, this is a test!"

# Start Flask server
python3 simple_hybrid_server.py --mode flask --port 5000

# Start MCP server
python3 simple_hybrid_server.py --mode mcp
```

## 📥 Installation

```bash
# Clone repository
git clone <your-repo-url>
cd azure_tts

# Install dependencies
pip install -r requirements_mcp.txt

# Copy and configure environment
cp .env.example .env
nano .env  # Add your Azure credentials
```

## ⚙️ Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `AZURE_SPEECH_KEY` | Yes | - | Azure Cognitive Services API key |
| `AZURE_SPEECH_REGION` | No | `eastus` | Azure region |
| `VOICE_NAME` | No | `en-US-GuyNeural` | Neural voice name |
| `VOICE_RATE` | No | `+0%` | Speech rate adjustment |
| `VOICE_PITCH` | No | `+0Hz` | Pitch adjustment |

### Available Voices

**Male Voices:**
- `en-US-GuyNeural` (Default)
- `en-US-DavisNeural`
- `en-US-JasonNeural`
- `en-US-TonyNeural`

**Female Voices:**
- `en-US-JennyNeural`
- `en-US-AriaNeural`
- `en-US-JaneNeural`
- `en-US-SaraNeural`

[Full voice list](https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support)

## 🎮 Usage

### MCP Mode

For integration with AI models:

**1. Add to MCP Configuration**

Claude Code (`~/.config/claude-code/mcp_settings.json`):
```json
{
  "mcpServers": {
    "azure-tts": {
      "command": "python3",
      "args": ["/absolute/path/to/simple_hybrid_server.py", "--mode", "mcp"]
    }
  }
}
```

**2. Use in AI Conversations**

The AI model can now call the `speak_text` tool automatically.

### Flask REST API Mode

**1. Start Server**

```bash
python3 simple_hybrid_server.py --mode flask --port 5000
```

**2. Send Requests**

```bash
# Basic request
curl -X POST http://localhost:5000/speak \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello, world!"}' \
  --output speech.wav

# With custom voice
curl -X POST http://localhost:5000/speak \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello!", "voice":"en-US-JennyNeural"}' \
  --output speech.wav
```

## 🔗 Integration Examples

### With Ollama

```python
import requests
from speak_bluetooth import BluetoothTTS

tts = BluetoothTTS()

# Get response from Ollama
response = requests.post(
    "http://localhost:11434/api/generate",
    json={"model": "llama3.2", "prompt": "Explain quantum computing", "stream": False}
)

text = response.json()["response"]
tts.speak(text)
```

### With Claude (via MCP)

Configure MCP as shown above, then Claude can automatically use TTS.

## 📚 API Reference

### MCP Tools

#### `speak_text`

**Parameters:**
- `text` (string, required): Text to speak
- `voice` (string, optional): Voice name
- `wait` (boolean, optional): Wait for completion

### REST API Endpoints

#### `POST /speak`

Generate speech audio from text.

**Request:**
```json
{
  "text": "Text to speak",
  "voice": "en-US-GuyNeural"
}
```

**Response:** WAV audio file

#### `GET /health`

Health check endpoint.

## 🤝 Contributing

Contributions welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md).

## 📄 License

MIT License - see [LICENSE](LICENSE) file.

---

**Made with ❤️ for the AI community**
