#!/usr/bin/env python3
"""
Azure TTS Flask Server with VLC Streaming
Receives text from any AI model, converts to speech, streams to VLC
"""

from flask import Flask, request, jsonify, send_file
import azure.cognitiveservices.speech as speechsdk
import os
import tempfile
from datetime import datetime

app = Flask(__name__)

# Load Azure credentials from .env file in same directory
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
DEFAULT_VOICE = os.getenv('VOICE_NAME', 'en-US-GuyNeural')

@app.route('/speak', methods=['POST'])
def speak():
    """Convert text to speech and return audio file"""
    data = request.json
    text = data.get('text', '')

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    if not SPEECH_KEY:
        return jsonify({'error': 'AZURE_SPEECH_KEY not set'}), 500

    # Configure Azure Speech
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    speech_config.speech_synthesis_voice_name = data.get('voice', DEFAULT_VOICE)

    # Create temp file for audio
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    audio_config = speechsdk.audio.AudioOutputConfig(filename=temp_file.name)

    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    result = synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return send_file(temp_file.name, mimetype='audio/wav')
    else:
        return jsonify({'error': f'Speech synthesis failed: {result.reason}'}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'running',
        'timestamp': datetime.now().isoformat(),
        'azure_configured': bool(SPEECH_KEY)
    })

if __name__ == '__main__':
    # Run on all interfaces so accessible via Tailscale
    app.run(host='0.0.0.0', port=5000, debug=False)
