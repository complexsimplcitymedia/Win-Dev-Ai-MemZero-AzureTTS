# How This Works (Explained Like You're 5)

> **TL;DR:** You talk to AI. AI remembers everything. AI talks back. Works on all your devices.

## 🎯 The Super Simple Version

### What Problem Are We Solving?

**Before (The Bad Way):**
```
You: "My name is Alex"
AI: "Nice to meet you, Alex!"

[Close app]
[Open app again]

You: "What's my name?"
AI: "I don't know 🤷"
```

**After (The Good Way - This Project):**
```
You: "My name is Alex"
AI: "Saved to memory!"

[Close app]
[Open app on different device]
[Even use a different AI]

You: "What's my name?"
AI: "Your name is Alex 🎯"
```

**The AI remembers you. Forever. Everywhere.**

---

## 🎨 Visual Flow Diagrams

### 1. How Voice In Works

```
     YOU                    COMPUTER                   AI
      │                         │                      │
      │   "Hey, what's 2+2?"   │                      │
      ├────────────────────────>│                      │
      │                         │                      │
      │                         │   [Sends text]       │
      │                         ├─────────────────────>│
      │                         │                      │
      │                         │   [AI thinks...]     │
      │                         │   "2+2 equals 4"     │
      │                         │<─────────────────────┤
      │                         │                      │
      │   🔊 "Two plus two      │                      │
      │      equals four"       │                      │
      │<────────────────────────┤                      │
      │                         │                      │
```

### 2. How Memory Works

```
┌─────────────┐       ┌──────────────┐       ┌──────────────┐
│   PHONE     │       │   MEMORY     │       │   COMPUTER   │
│             │       │   SERVER     │       │              │
│  "My fav    │──────>│              │<──────│  "What's my  │
│   color is  │ Saves │  🧠 Stores:  │ Reads │   favorite   │
│   blue"     │       │  Color=Blue  │       │   color?"    │
│             │       │              │       │              │
└─────────────┘       └──────────────┘       └──────────────┘
                             │
                             │ Same memory!
                             ▼
                      ┌──────────────┐
                      │    TABLET    │
                      │              │
                      │  "What color │
                      │   do I like?"│
                      │  → "Blue!"   │
                      └──────────────┘
```

### 3. Complete System Flow

```
┌────────────────────────────────────────────────────────────┐
│                         YOU                                │
│              (Talk or Type)                                │
└───────────────┬────────────────────────────────────────────┘
                │
                ▼
        ┌───────────────┐
        │   YOUR WORDS  │
        │ "Hey AI, help"│
        └───────┬───────┘
                │
                ▼
┌───────────────────────────────────────────────────────────┐
│                      MCP LAYER                            │
│  (This connects everything together - like a switchboard) │
└───────┬────────────────┬──────────────┬───────────────────┘
        │                │              │
        ▼                ▼              ▼
   ┌────────┐      ┌─────────┐    ┌────────┐
   │ MEMORY │      │  VOICE  │    │  TOOLS │
   │  🧠    │      │   🔊    │    │   🔧   │
   │        │      │         │    │        │
   │ Stores │      │ Azure   │    │ Code,  │
   │  your  │      │  TTS    │    │ Web,   │
   │  stuff │      │ Speaks  │    │ etc    │
   └────────┘      └─────────┘    └────────┘
        │                │              │
        └────────────┬───┴──────────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │       AI MODELS        │
        │  Claude │ Ollama │ etc │
        │  (Pick whichever!)     │
        └────────────────────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │       ANSWER           │
        │  "Here's what I found" │
        └────────┬───────────────┘
                 │
                 ▼
              🔊 SPEAKS TO YOU
```

---

## 🚀 Installation (The Easy Way)

### Step 1: Get the Code
```bash
# Just copy-paste this:
git clone <this-repo>
cd azure_tts
```

### Step 2: Get Your (Free) Azure Key
1. Go to https://portal.azure.com
2. Click "Create a resource"
3. Search "Speech"
4. Click "Create"
5. Copy your key

### Step 3: Setup
```bash
# Copy the example config
cp .env.example .env

# Edit it (paste your Azure key)
nano .env
```

Change this line:
```
AZURE_SPEECH_KEY=your_azure_speech_key_here
```

To:
```
AZURE_SPEECH_KEY=paste_your_actual_key_here
```

Save and exit (Ctrl+X, then Y, then Enter)

### Step 4: Install
```bash
# One command installs everything:
pip install -r requirements_mcp.txt
```

### Step 5: Test It!
```bash
# Make the AI talk:
python3 speak_bluetooth.py "Hello! I am working!"
```

**Did you hear a voice? ✅ It's working!**

---

## 🎯 How To Use It

### Mode 1: Direct Python
```bash
# Make AI say anything:
python3 speak_bluetooth.py "Your text here"

# Or pipe from other commands:
echo "Hello world" | python3 speak_bluetooth.py
```

### Mode 2: Flask Server (REST API)
```bash
# Start the server:
python3 simple_hybrid_server.py --mode flask --port 5000

# In another terminal, send text:
curl -X POST http://localhost:5000/speak \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello from the server!"}' \
  --output speech.wav

# Play it:
vlc speech.wav
```

### Mode 3: MCP (For AI Models)

Add to your AI's config:
```json
{
  "mcpServers": {
    "tts": {
      "command": "python3",
      "args": ["/full/path/to/simple_hybrid_server.py", "--mode", "mcp"]
    }
  }
}
```

Now your AI can speak!

### Mode 4: Toggle On/Off (Ctrl+Alt+T)
```bash
# Start the toggle service:
./start_tts_toggle.sh

# Now press Ctrl+Alt+T to turn TTS on/off
```

---

## 🔧 Troubleshooting (When Stuff Breaks)

### "I don't hear anything!"

**Check 1:** Is your Azure key correct?
```bash
# Look at your .env file:
cat .env

# Should say your actual key, not "your_azure_speech_key_here"
```

**Check 2:** Is Bluetooth connected?
- Windows: Check system tray
- Your headphones should show "Connected"

**Check 3:** Run test:
```bash
python3 speak_bluetooth.py "Testing one two three"
# Do you hear it? If not...
```

**Check 4:** Is the audio file created?
```bash
ls -la /mnt/c/Users/YOUR_USERNAME/tts_audio/
# Should see speech.wav
# If yes, file is created but not playing
# If no, Azure TTS is not working
```

### "Command not found: python3"

Try `python` instead:
```bash
python speak_bluetooth.py "Test"
```

Or install Python:
- Windows: https://www.python.org/downloads/
- Mac: `brew install python3`
- Linux: `sudo apt install python3`

### "ModuleNotFoundError: azure"

Install dependencies again:
```bash
pip install -r requirements_mcp.txt
```

### "Permission denied"

Make scripts executable:
```bash
chmod +x *.py *.sh
```

---

## 📖 Component Breakdown

### What Each File Does

| File | What It Does | Do You Need It? |
|------|--------------|-----------------|
| `speak_bluetooth.py` | Makes AI talk via Bluetooth | ✅ Yes |
| `simple_hybrid_server.py` | Main server (MCP + Flask) | ✅ Yes |
| `tts_toggle.py` | Ctrl+Alt+T to toggle TTS | Optional |
| `engine.py` | Azure TTS connection | ✅ Yes (auto-used) |
| `config.py` | Reads your .env file | ✅ Yes (auto-used) |
| `.env` | Your Azure key (SECRET!) | ✅ YES - Create this! |
| `.env.example` | Template for .env | Just for copying |

### What Each Technology Does

**Azure TTS:**
- Takes text
- Makes it sound like a human voice
- Outputs audio file

**MCP (Model Context Protocol):**
- Universal language for AI tools
- Like USB ports for AI
- Any AI can plug in

**Flask:**
- Makes a web server
- Listens for requests
- Sends back audio

**Bluetooth/Audio:**
- Gets audio to your ears
- Works with headphones, speakers, etc.

---

## 🎓 Advanced: Adding Memory

Want AI that remembers? Add mem0:

```bash
# Install mem0
docker-compose -f /path/to/mem0/docker-compose.yml up -d

# Now AI remembers everything!
```

Memory flow:
```
You say: "My birthday is June 15"
         ↓
    MCP receives it
         ↓
    Sends to memory server
         ↓
    Stored in database
         ↓
    [Days later]
         ↓
You ask: "When's my birthday?"
         ↓
    MCP checks memory
         ↓
    Finds: "June 15"
         ↓
    AI says: "Your birthday is June 15"
         ↓
    TTS speaks it to you
```

---

## 🎯 Quick Reference

### Start TTS Server
```bash
python3 simple_hybrid_server.py --mode flask --port 5000
```

### Make AI Speak
```bash
python3 speak_bluetooth.py "Your message"
```

### Toggle TTS On/Off
```bash
./start_tts_toggle.sh
# Then press Ctrl+Alt+T
```

### Check if Working
```bash
curl http://localhost:5000/health
```

### Stop Server
```bash
# Find process:
ps aux | grep simple_hybrid_server

# Kill it:
kill <PID>
```

---

## 💡 Tips & Tricks

### Change Voice

Edit `.env`:
```bash
# Male voices:
VOICE_NAME=en-US-GuyNeural      # Default
VOICE_NAME=en-US-DavisNeural    # Deeper
VOICE_NAME=en-US-JasonNeural    # Younger
VOICE_NAME=en-US-TonyNeural     # News anchor

# Female voices:
VOICE_NAME=en-US-JennyNeural    # Friendly
VOICE_NAME=en-US-AriaNeural     # Professional
VOICE_NAME=en-US-JaneNeural     # Warm
VOICE_NAME=en-US-SaraNeural     # Clear
```

### Change Speed

Edit `.env`:
```bash
VOICE_RATE=+0%      # Normal (default)
VOICE_RATE=+25%     # Faster
VOICE_RATE=-25%     # Slower
VOICE_RATE=+50%     # Very fast
```

### Change Pitch

Edit `.env`:
```bash
VOICE_PITCH=+0Hz    # Normal (default)
VOICE_PITCH=+10Hz   # Higher
VOICE_PITCH=-10Hz   # Lower
```

---

## 🆘 Still Stuck?

1. **Read error messages** - They usually tell you what's wrong
2. **Check the logs** - Look for red text
3. **Google the error** - Someone probably solved it
4. **Ask for help** - Open an issue on GitHub
5. **Check Azure** - Is your key valid? quota remaining?

---

## 🎉 Success Checklist

- [ ] Installed Python
- [ ] Got Azure key
- [ ] Created `.env` file
- [ ] Installed dependencies
- [ ] Ran test - heard voice
- [ ] Started server - no errors
- [ ] Sent test request - got audio
- [ ] Bluetooth connected
- [ ] Everything works!

**If all checked: You're done! 🎉**

---

**Remember:** If a 5-year-old can understand it, anyone can use it.

That's the goal. Keep it simple. Keep it free. Keep it open.
