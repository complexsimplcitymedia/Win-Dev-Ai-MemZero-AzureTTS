#!/bin/bash
# Start TTS Toggle Service in background
# Allows Ctrl+Alt+T to toggle TTS on/off system-wide

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Starting TTS Toggle Service..."
echo "Press Ctrl+Alt+T to toggle TTS on/off"
echo "Service will run in background"

# Install dependencies if needed
pip install -q pynput 2>/dev/null

# Start toggle service
python3 "$SCRIPT_DIR/tts_toggle.py" &
TTS_PID=$!

echo "✓ TTS Toggle Service started (PID: $TTS_PID)"
echo "  Run 'kill $TTS_PID' to stop"
echo "  Or use: pkill -f tts_toggle.py"

# Save PID
echo $TTS_PID > /tmp/tts_toggle.pid
