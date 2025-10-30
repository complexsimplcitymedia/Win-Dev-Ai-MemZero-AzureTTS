"""
Advanced TTS Example

Demonstrates advanced text-to-speech capabilities including:
- Multiple voices
- SSML markup
- Audio file generation
- Custom speech parameters
"""

import os
import logging
from win_dev_ai import AzureTTSEngine
from win_dev_ai.azure_tts import AudioFormat

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Demonstrate advanced TTS features."""
    
    print("Advanced Azure TTS Example")
    print("=" * 70)
    
    # Initialize TTS engine
    tts = AzureTTSEngine(
        default_voice="en-US-AriaNeural"
    )
    
    if not tts._speech_config:
        print("\n⚠ Azure credentials not configured!")
        print("Set the following environment variables:")
        print("  - AZURE_SPEECH_KEY: Your Azure Speech Service key")
        print("  - AZURE_SPEECH_REGION: Your Azure region (e.g., eastus)")
        return
    
    # 1. List available voices
    print("\n1. Available Voices")
    print("-" * 70)
    voices = tts.get_available_voices()
    # Note: Voice names are public Azure TTS identifiers, not sensitive data
    for voice in voices[:5]:
        print(f"  • {voice['name']} ({voice['gender']}, {voice['locale']})")
    
    # 2. Synthesize with different voices
    print("\n2. Testing Different Voices")
    print("-" * 70)
    
    test_text = "Hello! This is a test of the Azure Text to Speech system."
    
    for voice_name in ["en-US-JennyNeural", "en-US-GuyNeural"]:
        print(f"\nSpeaking with {voice_name}...")
        tts.set_voice(voice_name)
        # Uncomment to actually speak:
        # tts.synthesize_to_speaker(test_text)
        print(f"  ✓ Voice set to {voice_name}")
    
    # 3. Use SSML for advanced control
    print("\n3. SSML Examples")
    print("-" * 70)
    
    # Create SSML with different rates
    for rate in ["slow", "medium", "fast"]:
        ssml = tts.create_ssml(
            "This is a demonstration of speech rate control.",
            voice="en-US-AriaNeural",
            rate=rate,
            pitch="medium"
        )
        print(f"\n{rate.capitalize()} speech SSML:")
        print(ssml[:100] + "...")
    
    # 4. Save to audio files
    print("\n4. Saving Audio Files")
    print("-" * 70)
    
    # Create output directory
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Save with different formats
    formats = [
        (AudioFormat.WAV_16KHZ, "output/sample_16khz.wav"),
        (AudioFormat.MP3_128KBPS, "output/sample.mp3"),
    ]
    
    for audio_format, filename in formats:
        print(f"\nSaving {filename}...")
        tts.set_audio_format(audio_format)
        
        # Create interesting content with SSML
        content = tts.create_ssml(
            "Welcome to the Win Dev AI framework. "
            "This system combines secure memory management with "
            "Azure Text to Speech capabilities.",
            rate="medium",
            pitch="medium"
        )
        
        # Save the file
        success = tts.synthesize_to_file(content, filename, use_ssml=True)
        
        if success:
            print(f"  ✓ Audio saved to {filename}")
        else:
            print(f"  ✗ Failed to save {filename}")
    
    # 5. Test connection
    print("\n5. Connection Test")
    print("-" * 70)
    
    if tts.test_connection():
        print("✓ Azure TTS connection successful!")
    else:
        print("✗ Azure TTS connection failed")
    
    print("\n" + "=" * 70)
    print("Advanced TTS example completed!")


if __name__ == "__main__":
    main()
