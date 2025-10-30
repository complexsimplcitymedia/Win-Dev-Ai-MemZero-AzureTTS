#!/usr/bin/env python3
"""
MCP TTS Server - Universal Text-to-Speech via MCP Protocol
Provides speak_text tool to any MCP-compatible AI model
"""

import asyncio
import sys
import os
from typing import Any

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Import existing Azure TTS engine
from engine import AzureTTS
from config import TTSConfig

# Initialize server
server = Server("azure-tts")

# Initialize TTS engine (loads from .env)
tts_engine = None

def get_tts():
    """Lazy load TTS engine"""
    global tts_engine
    if tts_engine is None:
        tts_engine = AzureTTS()
    return tts_engine

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
                        "description": "Voice name (default: en-US-GuyNeural for male, en-US-JennyNeural for female)",
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
        # Common Azure neural voices
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

async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
