#!/usr/bin/env python3
"""
Hybrid TTS Server - Supports both MCP (STDIO) and Flask (REST API)
Run with --mcp for MCP mode, or --flask for Flask mode (default: Flask)
"""

import asyncio
import sys
import os
import argparse
from typing import Any
import tempfile

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Load .env file
env_file = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line and '```' not in line:
                key, value = line.split('=', 1)
                os.environ[key] = value.strip()

# Import after env is loaded
import config as config_module
import engine as engine_module

AzureTTS = engine_module.AzureTTS
TTSConfig = config_module.TTSConfig

# Initialize TTS engine
tts_engine = None

def get_tts():
    """Lazy load TTS engine"""
    global tts_engine
    if tts_engine is None:
        tts_engine = AzureTTS()
    return tts_engine

# ============================================================================
# FLASK MODE
# ============================================================================

def run_flask(host='0.0.0.0', port=5000):
    """Run as Flask REST API server"""
    from flask import Flask, request, jsonify, send_file
    from datetime import datetime

    app = Flask(__name__)

    @app.route('/speak', methods=['POST'])
    def speak():
        """Convert text to speech and return audio file"""
        data = request.json
        text = data.get('text', '')
        voice = data.get('voice', None)

        if not text:
            return jsonify({'error': 'No text provided'}), 400

        try:
            tts = get_tts()

            # Set voice if specified
            if voice and voice != tts.config.voice_name:
                tts.set_voice(voice)

            # Create temp file for audio
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')

            # Import Azure SDK for file output
            import azure.cognitiveservices.speech as speechsdk

            # Configure for file output
            audio_config = speechsdk.audio.AudioOutputConfig(filename=temp_file.name)
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=tts.speech_config,
                audio_config=audio_config
            )

            # Build SSML
            ssml = tts._build_ssml(text)
            result = synthesizer.speak_ssml_async(ssml).get()

            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                return send_file(temp_file.name, mimetype='audio/wav')
            else:
                return jsonify({'error': f'Speech synthesis failed: {result.reason}'}), 500

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/health', methods=['GET'])
    def health():
        """Health check endpoint"""
        tts = get_tts()
        return jsonify({
            'status': 'running',
            'mode': 'flask',
            'timestamp': datetime.now().isoformat(),
            'voice': tts.config.voice_name
        })

    print("=" * 60)
    print("Azure TTS Hybrid Server - FLASK MODE")
    print("=" * 60)
    print(f"Listening on: {host}:{port}")
    print(f"Voice: {get_tts().config.voice_name}")
    print()
    print("Endpoints:")
    print(f"  POST /speak - Convert text to speech")
    print(f"  GET  /health - Health check")
    print()
    print("Example:")
    print(f'  curl -X POST http://localhost:{port}/speak \\')
    print('    -H "Content-Type: application/json" \\')
    print('    -d \'{"text":"Hello from Flask TTS"}\' \\')
    print('    --output test.wav && vlc.exe test.wav')
    print("=" * 60)

    app.run(host=host, port=port, debug=False)

# ============================================================================
# MCP MODE
# ============================================================================

async def run_mcp():
    """Run as MCP STDIO server"""
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent

    server = Server("azure-tts")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available TTS tools"""
        return [
            Tool(
                name="speak_text",
                description="Convert text to speech using Azure TTS. Speaks the text aloud with configurable voice.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "The text to speak aloud"
                        },
                        "voice": {
                            "type": "string",
                            "description": "Voice name (default: en-US-GuyNeural for male)",
                            "default": "en-US-GuyNeural"
                        },
                        "wait": {
                            "type": "boolean",
                            "description": "Whether to wait for speech to complete (default: true)",
                            "default": True
                        }
                    },
                    "required": ["text"]
                }
            ),
            Tool(
                name="list_voices",
                description="List available Azure TTS voices",
                inputSchema={
                    "type": "object",
                    "properties": {}
                }
            )
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: Any) -> list[TextContent]:
        """Handle tool calls"""

        if name == "speak_text":
            text = arguments.get("text", "")
            voice = arguments.get("voice", "en-US-GuyNeural")
            wait = arguments.get("wait", True)

            if not text:
                return [TextContent(type="text", text="Error: No text provided")]

            try:
                tts = get_tts()

                # Set voice if different from default
                if voice != tts.config.voice_name:
                    tts.set_voice(voice)

                # Speak the text
                success = tts.speak(text, wait=wait)

                if success:
                    return [TextContent(
                        type="text",
                        text=f"✓ Spoke {len(text)} characters with voice: {voice}"
                    )]
                else:
                    return [TextContent(
                        type="text",
                        text="✗ Speech synthesis failed"
                    )]

            except Exception as e:
                return [TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )]

        elif name == "list_voices":
            voices = [
                "en-US-GuyNeural (Male)",
                "en-US-JennyNeural (Female)",
                "en-US-AriaNeural (Female)",
                "en-US-DavisNeural (Male)",
                "en-US-JaneNeural (Female)",
                "en-US-JasonNeural (Male)",
                "en-US-SaraNeural (Female)",
                "en-US-TonyNeural (Male)",
            ]
            return [TextContent(
                type="text",
                text="Available voices:\n" + "\n".join(voices)
            )]

        else:
            return [TextContent(
                type="text",
                text=f"Unknown tool: {name}"
            )]

    print("Azure TTS Hybrid Server - MCP MODE", file=sys.stderr)
    print(f"Voice: {get_tts().config.voice_name}", file=sys.stderr)

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description='Hybrid TTS Server')
    parser.add_argument('--mode', choices=['flask', 'mcp'], default='flask',
                       help='Server mode (default: flask)')
    parser.add_argument('--host', default='0.0.0.0',
                       help='Flask host (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=5000,
                       help='Flask port (default: 5000)')

    args = parser.parse_args()

    if args.mode == 'flask':
        run_flask(host=args.host, port=args.port)
    else:
        asyncio.run(run_mcp())

if __name__ == "__main__":
    main()
