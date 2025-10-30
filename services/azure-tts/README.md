# 🎙️ Azure TTS - Cadillac Voice for AI

> **Premium text-to-speech that actually sounds human.** Built for AI assistants, command-line tools, and everything in between.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Azure Speech](https://img.shields.io/badge/Azure-Cognitive%20Services-0078D4)](https://azure.microsoft.com/services/cognitive-services/text-to-speech/)
[![GitHub](https://img.shields.io/badge/GitHub-complexsimplcitymedia-181717?logo=github)](https://github.com/complexsimplcitymedia/TTS-audio)

**Wolf-level performance. Cadillac-level quality.**

---

## ✨ What Makes This Different

🎯 **Zero-config deployment** - Set two env vars, you're done  
🚀 **Command-line native** - Pipe anything to speech in one line  
🤖 **AI-first design** - Stream LLM responses directly to audio  
🎵 **48kHz neural audio** - HD voices that don't sound robotic  
🌍 **100+ languages** - One API, global reach  
⚡ **Stupid fast** - Low latency, high throughput  

---

## 🔥 Quick Start

### Install

```bash
# Clone or add as submodule
git submodule add https://github.com/complexsimplcitymedia/TTS-audio.git azure_tts

# Install dependencies
pip install azure-cognitiveservices-speech
```

### Configure (2 env vars, that's it)
```bash
# Linux/Mac/WSL
export AZURE_SPEECH_KEY="your_key_here"
export AZURE_SPEECH_REGION="eastus"

# Windows PowerShell
$env:AZURE_SPEECH_KEY="your_key_here"
$env:AZURE_SPEECH_REGION="eastus"
```

👉 Get free Azure key: [portal.azure.com](https://portal.azure.com)

### Use It

**Instant CLI magic:**
```bash
# Speak anything
python -m azure_tts.cli "This is wild"

# Pipe from anywhere
echo "Making my terminal talk" | python -m azure_tts.cli --stdin

# Different voices
python -m azure_tts.cli --voice en-US-GuyNeural "Deep voice activated"

# Interactive mode
python -m azure_tts.cli -i
```

**Python integration:**
```python
from azure_tts import AzureTTS

tts = AzureTTS()
tts.speak("Simple as that")

# Customize everything
tts.set_voice("en-US-JennyNeural")
tts.set_rate("+20%")  # Speed it up
tts.speak("Faster talking now")
```

---

## 💡 Real-World Use Cases

### 🤖 AI Assistant Voice
```python
import ollama
from azure_tts import AzureTTS

tts = AzureTTS()
response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': 'Tell me a joke'}])
tts.speak(response['message']['content'])
```

### 🌊 Stream Live AI Responses
```python
from openai import OpenAI
from azure_tts import AzureTTS

client = OpenAI()
tts = AzureTTS()

stream = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Explain quantum computing"}],
    stream=True
)

def stream_text():
    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

tts.speak_stream(stream_text())  # Speaks as it generates
```

### ⚡ Command Line Wizardry
```bash
# Make git talk
git log --oneline -5 | python -m azure_tts.cli --stdin

# Verbal notifications
curl -s wttr.in/London?format=3 | python -m azure_tts.cli --stdin

# Read docs aloud
cat CONTRIBUTING.md | python -m azure_tts.cli --stdin

# Speak command output
df -h | python -m azure_tts.cli --stdin
```

---

## 🎛️ Configuration

### Environment Variables
```bash
AZURE_SPEECH_KEY=<required>           # Your Azure Speech key
AZURE_SPEECH_REGION=eastus            # Azure region
VOICE_NAME=en-US-AvaMultilingualNeural  # Optional: default voice
VOICE_RATE=+0%                        # Optional: -50% to +100%
VOICE_PITCH=+0Hz                      # Optional: -50Hz to +50Hz
```

### 🎤 Premium Voice Collection
- **`en-US-AvaMultilingualNeural`** - Natural conversational (default)
- **`en-US-JennyNeural`** - Warm & friendly
- **`en-US-GuyNeural`** - Deep & professional
- **`en-US-AriaNeural`** - Clear & upbeat
- **`en-US-DavisNeural`** - Calm & reassuring
- **`en-US-TonyNeural`** - News anchor style

[**Browse 100+ voices →**](https://learn.microsoft.com/azure/ai-services/speech-service/language-support?tabs=tts)

---

## 📦 Project Structure
```
azure_tts/
├── __init__.py          # Module exports
├── cli.py               # Command-line interface
├── config.py            # Zero-config setup
├── engine.py            # TTS engine core
└── setup_secrets.ps1    # Windows helper script
```

---

## 🔧 Use as Submodule

Perfect for embedding in larger AI projects:

```bash
# Add to your repo
git submodule add https://github.com/complexsimplcitymedia/TTS-audio.git modules/tts

# Import in code
from modules.tts import AzureTTS
```

---

## 🔒 Security Best Practices

✅ **Never commit credentials**  
✅ **Use environment variables only**  
✅ **`.env` files are gitignored**  
✅ **Rotate keys regularly**  
✅ **Use Azure Key Vault for production**  

---

## 📋 Requirements

- Python 3.10+
- `azure-cognitiveservices-speech`
- Active Azure Speech resource (free tier available)

---

## 🤝 Contributing

This module is built to be:
- **Minimal** - Does one thing exceptionally well
- **Portable** - Works standalone or embedded
- **Battle-tested** - Production-ready error handling

PRs welcome. Keep it clean, keep it fast.

---

## 📄 License

MIT - See [LICENSE](LICENSE)

---

<div align="center">

**Powered by Azure Cognitive Services**

[Get Started](https://azure.microsoft.com/services/cognitive-services/text-to-speech/) · [Documentation](https://learn.microsoft.com/azure/ai-services/speech-service/) · [GitHub](https://github.com/complexsimplcitymedia/TTS-audio)

</div>
