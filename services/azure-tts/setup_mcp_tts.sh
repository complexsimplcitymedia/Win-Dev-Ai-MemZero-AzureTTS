#!/bin/bash
# Setup MCP TTS Server for Universal AI Voice

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MCP_SERVER="$SCRIPT_DIR/mcp_tts_server.py"

echo "=================================="
echo "MCP TTS Server Setup"
echo "=================================="

# Install dependencies
echo "Installing Python dependencies..."
pip install -q mcp azure-cognitiveservices-speech

# Make server executable
chmod +x "$MCP_SERVER"

echo ""
echo "✓ MCP TTS Server installed at:"
echo "  $MCP_SERVER"
echo ""
echo "=================================="
echo "Configuration Instructions"
echo "=================================="
echo ""
echo "Add this to your MCP config file:"
echo ""
echo "For Claude Code (~/.config/claude-code/mcp_settings.json):"
echo ""
cat << EOF
{
  "mcpServers": {
    "azure-tts": {
      "command": "python3",
      "args": ["$MCP_SERVER"]
    }
  }
}
EOF
echo ""
echo "For Ollama/other models, add similar config to their MCP settings."
echo ""
echo "=================================="
echo "Tools Available:"
echo "=================================="
echo "  - speak_text: Convert text to speech"
echo "  - list_voices: List available voices"
echo ""
echo "✓ Setup complete!"
