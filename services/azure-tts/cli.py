"""
CLI interface for Azure TTS
"""

import sys
import argparse
from .engine import AzureTTS
from .config import TTSConfig

def speak_stdin(tts: AzureTTS):
    """Read from stdin and speak"""
    print("Azure TTS: Reading from stdin...")
    for line in sys.stdin:
        text = line.strip()
        if text:
            tts.speak(text)

def speak_interactive(tts: AzureTTS):
    """Interactive mode"""
    print("Azure TTS Interactive Mode")
    print("Type text to speak, 'quit' to exit")
    print("-" * 50)
    
    while True:
        try:
            text = input("> ")
            if text.lower() in ['quit', 'exit', 'q']:
                break
            tts.speak(text)
        except KeyboardInterrupt:
            break
    
    print("\nExiting...")

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Azure TTS - Text-to-Speech for AI outputs'
    )
    parser.add_argument('text', nargs='*', help='Text to speak')
    parser.add_argument('-i', '--interactive', action='store_true',
                       help='Interactive mode')
    parser.add_argument('-s', '--stdin', action='store_true',
                       help='Read from stdin (pipe mode)')
    parser.add_argument('--voice', help='Voice name')
    parser.add_argument('--rate', help='Speaking rate (e.g., +10%%)')
    parser.add_argument('--pitch', help='Voice pitch (e.g., +5Hz)')
    
    args = parser.parse_args()
    
    # Initialize TTS
    try:
        config = TTSConfig()
        
        if args.voice:
            config.voice_name = args.voice
        if args.rate:
            config.voice_rate = args.rate
        if args.pitch:
            config.voice_pitch = args.pitch
        
        tts = AzureTTS(config)
        
    except SystemExit:
        print("\n💡 Set AZURE_SPEECH_KEY in .env file")
        sys.exit(1)
    
    # Handle modes
    if args.interactive:
        speak_interactive(tts)
    elif args.stdin or not sys.stdin.isatty():
        speak_stdin(tts)
    elif args.text:
        text = ' '.join(args.text)
        success = tts.speak(text)
        sys.exit(0 if success else 1)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
