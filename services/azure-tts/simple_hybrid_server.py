#!/usr/bin/env python3
"""
Simple Hybrid TTS Server - MCP + Flask, no complex imports
"""

import asyncio
import sys
import os
import argparse
import tempfile
import azure.cognitiveservices.speech as speechsdk

# Load .env
env_file = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line and '```' not in line:
                key, value = line.split('=', 1)
                os.environ[key] = value.strip()

SPEECH_KEY = os.getenv('AZURE_SPEECH_KEY')
SPEECH_REGION = os.getenv('AZURE_SPEECH_REGION', 'eastus')
VOICE_NAME = os.getenv('VOICE_NAME', 'en-US-GuyNeural')

def speak_text(text, voice=None):
    """Speak text using Azure TTS via Bluetooth"""
    import subprocess
    from pathlib import Path

    if not voice:
        voice = VOICE_NAME

    # Shared folder for Windows Bluetooth playback
    audio_dir = Path("/mnt/c/Users/D_ADA/tts_audio")
    audio_dir.mkdir(exist_ok=True)
    audio_file = audio_dir / "speech.wav"

    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    speech_config.speech_synthesis_voice_name = voice
    audio_config = speechsdk.audio.AudioOutputConfig(filename=str(audio_file))

    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config,
        audio_config=audio_config
    )

    result = synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        # Play via Windows PowerShell (Bluetooth supported)
        windows_path = str(audio_file).replace('/mnt/c/', 'C:\\').replace('/', '\\')
        ps_command = f'$player = New-Object System.Media.SoundPlayer "{windows_path}"; $player.PlaySync()'

        try:
            subprocess.run(
                ['powershell.exe', '-Command', ps_command],
                check=True,
                capture_output=True,
                timeout=30
            )
            return True
        except Exception as e:
            print(f"Playback error: {e}", file=sys.stderr)
            return False

    return False

def speak_to_file(text, filename, voice=None):
    """Speak text and save to file"""
    if not voice:
        voice = VOICE_NAME

    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    speech_config.speech_synthesis_voice_name = voice
    audio_config = speechsdk.audio.AudioOutputConfig(filename=filename)

    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config,
        audio_config=audio_config
    )

    result = synthesizer.speak_text_async(text).get()
    return result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted

# =============================================================================
# FLASK MODE
# =============================================================================

def run_flask(host='0.0.0.0', port=5000):
    from flask import Flask, request, jsonify, send_file
    from datetime import datetime

    app = Flask(__name__)

    @app.route('/speak', methods=['POST'])
    def speak():
        data = request.json
        text = data.get('text', '')
        voice = data.get('voice', VOICE_NAME)

        if not text:
            return jsonify({'error': 'No text provided'}), 400

        try:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            success = speak_to_file(text, temp_file.name, voice)

            if success:
                return send_file(temp_file.name, mimetype='audio/wav')
            else:
                return jsonify({'error': 'Speech synthesis failed'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({
            'status': 'running',
            'mode': 'flask',
            'voice': VOICE_NAME,
            'timestamp': datetime.now().isoformat()
        })

    print("=" * 60)
    print("Azure TTS Server - FLASK MODE")
    print("=" * 60)
    print(f"Listening on: {host}:{port}")
    print(f"Voice: {VOICE_NAME}")
    print()
    print("Test:")
    print(f'  curl -X POST http://localhost:{port}/speak \\')
    print('    -H "Content-Type: application/json" \\')
    print('    -d \'{"text":"Hello, this is a test"}\' \\')
    print('    --output test.wav && vlc.exe test.wav')
    print("=" * 60)

    app.run(host=host, port=port, debug=False)

# =============================================================================
# MCP MODE
# =============================================================================

async def run_mcp():
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent

    server = Server("azure-tts")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="speak_text",
                description="Speak text aloud using Azure TTS",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "Text to speak"},
                        "voice": {"type": "string", "description": "Voice name", "default": VOICE_NAME}
                    },
                    "required": ["text"]
                }
            )
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        if name == "speak_text":
            text = arguments.get("text", "")
            voice = arguments.get("voice", VOICE_NAME)

            if not text:
                return [TextContent(type="text", text="Error: No text provided")]

            try:
                success = speak_text(text, voice)
                if success:
                    return [TextContent(type="text", text=f"✓ Spoke: {text[:50]}...")]
                else:
                    return [TextContent(type="text", text="✗ Speech failed")]
            except Exception as e:
                return [TextContent(type="text", text=f"Error: {e}")]

        return [TextContent(type="text", text=f"Unknown tool: {name}")]

    print("Azure TTS Server - MCP MODE", file=sys.stderr)
    print(f"Voice: {VOICE_NAME}", file=sys.stderr)

    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['flask', 'mcp'], default='flask')
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', type=int, default=5000)
    args = parser.parse_args()

    if args.mode == 'flask':
        run_flask(args.host, args.port)
    else:
        asyncio.run(run_mcp())

if __name__ == "__main__":
    main()
