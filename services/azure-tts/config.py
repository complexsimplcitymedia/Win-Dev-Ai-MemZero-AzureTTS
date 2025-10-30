"""
Configuration and secrets management for Azure TTS module
Reads from environment variables (never stores secrets in files)
"""

import os
import sys
from pathlib import Path
from typing import Dict

class TTSConfig:
    """Manages Azure TTS configuration"""
    
    def __init__(self):
        self.azure_key = self._get_required_env('AZURE_SPEECH_KEY')
        self.azure_region = os.getenv('AZURE_SPEECH_REGION', 'eastus')
        
        # Voice preferences (non-secret)
        self.voice_name = os.getenv('VOICE_NAME', 'en-US-AvaMultilingualNeural')
        self.voice_rate = os.getenv('VOICE_RATE', '+0%')
        self.voice_pitch = os.getenv('VOICE_PITCH', '+0Hz')
        
        # Local preferences file (no secrets)
        self.preferences_path = Path.home() / '.config' / 'azure-tts' / 'preferences.json'
        self._load_preferences()
    
    def _get_required_env(self, key: str) -> str:
        """Get required environment variable or exit"""
        value = os.getenv(key)
        if not value:
            print(f"❌ Error: {key} environment variable not set")
            print(f"Add to your .env file or shell profile:")
            print(f"export {key}='your_key_here'")
            sys.exit(1)
        return value
    
    def _load_preferences(self):
        """Load non-secret preferences from local file"""
        import json
        
        if self.preferences_path.exists():
            try:
                with open(self.preferences_path) as f:
                    prefs = json.load(f)
                    self.voice_name = prefs.get('voice_name', self.voice_name)
                    self.voice_rate = prefs.get('voice_rate', self.voice_rate)
                    self.voice_pitch = prefs.get('voice_pitch', self.voice_pitch)
            except Exception as e:
                print(f"Warning: Could not load preferences: {e}")
    
    def save_preferences(self):
        """Save non-secret preferences to local file"""
        import json
        
        self.preferences_path.parent.mkdir(parents=True, exist_ok=True)
        prefs = {
            'voice_name': self.voice_name,
            'voice_rate': self.voice_rate,
            'voice_pitch': self.voice_pitch
        }
        with open(self.preferences_path, 'w') as f:
            json.dump(prefs, f, indent=2)
    
    def to_dict(self) -> Dict[str, str]:
        """Export config as dict (without secrets)"""
        return {
            'voice_name': self.voice_name,
            'voice_rate': self.voice_rate,
            'voice_pitch': self.voice_pitch,
            'region': self.azure_region
        }
