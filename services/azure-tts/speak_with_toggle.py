#!/usr/bin/env python3
"""
TTS wrapper that respects the toggle state
Use this instead of speak_bluetooth.py for toggle support
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from speak_bluetooth import BluetoothTTS
from tts_toggle import is_tts_enabled

def main():
    """Main entry point with toggle check"""

    # Check if TTS is enabled
    if not is_tts_enabled():
        print("🔇 TTS is disabled (Ctrl+Alt+T to enable)")
        return

    # Get text from arguments or stdin
    if len(sys.argv) > 1:
        text = ' '.join(sys.argv[1:])
    else:
        text = sys.stdin.read().strip()

    if not text:
        print("Usage: speak_with_toggle.py \"text to speak\"")
        print("   or: echo \"text\" | speak_with_toggle.py")
        return

    # Speak it
    tts = BluetoothTTS()
    tts.speak(text)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n🔇 Stopped")
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
