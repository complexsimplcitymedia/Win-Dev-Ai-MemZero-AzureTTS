#!/bin/bash
# Simple helper to speak text via TTS server
# Usage: ./speak_helper.sh "text to speak"
# Or pipe: echo "text" | ./speak_helper.sh

TTS_SERVER="http://localhost:5000"

# Get text from argument or stdin
if [ $# -gt 0 ]; then
    TEXT="$*"
else
    TEXT=$(cat)
fi

if [ -z "$TEXT" ]; then
    echo "Usage: $0 \"text to speak\" or pipe text via stdin"
    exit 1
fi

# Send to TTS server and play with VLC
curl -s -X POST "$TTS_SERVER/speak" \
    -H "Content-Type: application/json" \
    -d "{\"text\":\"$TEXT\"}" \
    --output /tmp/tts_output.wav && \
    vlc.exe --play-and-exit --no-video-title-show /tmp/tts_output.wav 2>/dev/null &
