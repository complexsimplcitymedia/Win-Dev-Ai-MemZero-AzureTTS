# MCP TTS Server - Universal AI Voice

## What This Does

Provides **universal text-to-speech** via MCP protocol for ALL your AI models:
- Claude Code
- Ollama
- Gemini
- Any MCP-compatible client

**Same voice, same context, everywhere.**

## Setup

1. **Install the server:**
   ```bash
   cd /mnt/r/AI-Windows_Assistant-master/module-Cognitive-Speech-TTS/azure_tts
   ./setup_mcp_tts.sh
   ```

2. **Add to MCP config:**

   **For Claude Code:** `~/.config/claude-code/mcp_settings.json`
   ```json
   {
     "mcpServers": {
       "azure-tts": {
         "command": "python3",
         "args": ["/mnt/r/AI-Windows_Assistant-master/module-Cognitive-Speech-TTS/azure_tts/mcp_tts_server.py"]
       }
     }
   }
   ```

   **For other models:** Add similar config to their MCP settings

3. **Restart your AI client** to load the MCP server

## Usage

Once configured, AI models can call TTS tools:

**Example in Claude Code:**
```
You: "Read this aloud: The quick brown fox jumps over the lazy dog"
Claude: [calls speak_text tool with the text]
```

**Available Tools:**
- `speak_text(text, voice?, wait?)` - Speak text with Azure TTS
- `list_voices()` - Show available voices

## Architecture

```
┌─────────────────────────────────────┐
│ Any AI Model (Claude/Ollama/etc)   │
└────────────┬────────────────────────┘
             │ MCP Protocol (STDIO)
             ▼
┌─────────────────────────────────────┐
│  MCP TTS Server (this)              │
│  - STDIO communication              │
│  - No HTTP/network layer            │
│  - No timeouts                      │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  Azure Speech SDK                   │
│  - Text → Audio conversion          │
│  - Uses .env credentials            │
└────────────┬────────────────────────┘
             │
             ▼
       Audio Output

## Why MCP Instead of REST API?

**Old approach (Flask/REST):**
- AI → curl → HTTP → Flask → Azure → VLC
- Network timeouts
- Complex, brittle
- Custom per-model

**New approach (MCP/STDIO):**
- AI → STDIO → MCP Server → Azure → Audio
- No timeouts
- Standard protocol
- Universal

## Default Voice

Male voice: `en-US-GuyNeural` (from `.env`)

Change in `.env`:
```bash
VOICE_NAME=en-US-JennyNeural  # Female
VOICE_NAME=en-US-GuyNeural    # Male
```

## Combined with Memory

You now have:
- **Universal Memory** via `openmemory-mcp` (mem0)
- **Universal Voice** via `azure-tts` MCP server

All models share context AND voice.
