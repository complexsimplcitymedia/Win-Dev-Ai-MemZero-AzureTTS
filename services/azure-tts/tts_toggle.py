#!/usr/bin/env python3
"""
TTS Toggle Service with Ctrl+Alt+T Hotkey
Runs in background and toggles TTS on/off
"""

import os
import sys
import json
import signal
from pathlib import Path
from pynput import keyboard

# State file
STATE_FILE = Path.home() / ".config" / "azure-tts" / "tts_enabled.json"
STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

class TTSToggle:
    """TTS toggle service with hotkey support"""

    def __init__(self):
        self.enabled = self.load_state()
        self.print_status()

    def load_state(self):
        """Load TTS enabled state"""
        if STATE_FILE.exists():
            try:
                with open(STATE_FILE) as f:
                    data = json.load(f)
                    return data.get('enabled', True)
            except:
                return True
        return True

    def save_state(self):
        """Save TTS enabled state"""
        with open(STATE_FILE, 'w') as f:
            json.dump({'enabled': self.enabled}, f)

    def toggle(self):
        """Toggle TTS on/off"""
        self.enabled = not self.enabled
        self.save_state()
        self.print_status()

        # Send notification (optional)
        try:
            os.system(f'notify-send "TTS {"Enabled" if self.enabled else "Disabled"}"')
        except:
            pass

    def print_status(self):
        """Print current status"""
        status = "🔊 ENABLED" if self.enabled else "🔇 DISABLED"
        print(f"\r[TTS] {status}", end="", flush=True)

    def is_enabled(self):
        """Check if TTS is enabled"""
        return self.enabled

# Global instance
toggle_service = TTSToggle()

def on_activate():
    """Hotkey callback"""
    toggle_service.toggle()

def run_service():
    """Run the toggle service"""
    print("TTS Toggle Service Starting...")
    print("Hotkey: Ctrl+Alt+T to toggle TTS on/off")
    print("Press Ctrl+C to exit")
    print()

    # Setup hotkey
    with keyboard.GlobalHotKeys({
        '<ctrl>+<alt>+t': on_activate
    }) as hotkey_listener:
        try:
            hotkey_listener.join()
        except KeyboardInterrupt:
            print("\n\nTTS Toggle Service Stopped")
            sys.exit(0)

def is_tts_enabled():
    """Check if TTS is currently enabled (for use by other scripts)"""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE) as f:
                data = json.load(f)
                return data.get('enabled', True)
        except:
            return True
    return True

if __name__ == "__main__":
    # Handle signals
    signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))
    signal.signal(signal.SIGTERM, lambda s, f: sys.exit(0))

    run_service()
