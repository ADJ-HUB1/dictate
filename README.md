# Dictate

**Local, private, offline voice-to-text dictation for macOS.** Press a hotkey, speak, and watch cleaned text appear in any app — no internet required, completely free, and your voice never leaves your computer.

Inspired by [Wispr Flow](https://wisprflow.com), built with [faster-whisper](https://github.com/SYSTRAN/faster-whisper).

---

## ✨ Features

- **🔒 100% Private** — Everything runs locally using OpenAI's Whisper model. No data sent to servers.
- **⚡ Fast** — Transcribes 10 seconds of speech in ~1-3 seconds on Apple Silicon
- **🎯 Smart Cleanup** — Automatically removes filler words ("um", "uh", "like", "you know") and adds punctuation
- **🎛️ Two Recording Modes**:
  - **Toggle mode**: Press hotkey to start, press again to stop
  - **Hold-to-talk mode**: Hold hotkey while speaking, release to transcribe
- **📋 Universal Paste** — Works in any text field in any macOS app
- **🔔 Optional Feedback** — Sound beeps and preview notifications for better UX
- **🎛️ Configurable** — Choose model size, language, recording mode, and more

---

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/ADJ-HUB1/dictate.git
cd dictate
bash scripts/install.sh
```

The install script will:
1. Create a Python virtual environment
2. Install all dependencies
3. Copy `.env.example` to `.env`
4. You're ready to go!

### Manual Installation

If you prefer manual setup:

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e .

# Create configuration file
cp .env.example .env

# Run the app
python -m dictate
```

---

## 🎯 Usage

### First Run

1. **Start the app:**
   ```bash
   cd dictate
   source .venv/bin/activate
   python -m dictate
   ```

2. **Grant permissions** when macOS prompts you:
   - **Microphone** — Required for recording (automatic prompt)
   - **Accessibility** — Required for global hotkey and paste:
     - Open **System Settings → Privacy & Security → Accessibility**
     - Click the **+** button and add your terminal app (Terminal.app, iTerm, etc.)

3. **Look for the menu bar icon** — Dictate runs in your macOS menu bar

4. **Start dictating:**
   - **Toggle mode** (default): Press **Option+Space** to start recording, speak naturally, press **Option+Space** again to stop
   - **Hold-to-talk mode**: Hold **Option+Space** while speaking, release to transcribe and paste

### Tips for Best Results

- **Speak naturally** — No need to pause between words
- **Don't worry about filler words** — "um", "uh", "like", etc. are automatically removed
- **Punctuation is automatic** — The AI adds commas and periods for you
- **Wait for the beep** (if enabled) — The stop beep confirms recording has ended
- **First transcription is slower** — The Whisper model loads on first use (~2-3 seconds), then it's fast

---

## ⚙️ Configuration

Edit `.env` to customize your experience:

```bash
# Recording mode: "toggle" or "hold"
HOTKEY_MODE=toggle

# Whisper model: tiny, base, small, medium, large-v3
# Recommendation: "small" for best accuracy/speed balance
WHISPER_MODEL=small

# Enable sound feedback (beeps on start/stop)
ENABLE_SOUND_FEEDBACK=true

# Show preview notification before pasting
SHOW_PREVIEW_NOTIFICATION=false
```

### Model Size Guide

| Model | RAM Usage | Speed | Accuracy | Best For |
|-------|-----------|-------|----------|----------|
| `tiny` | ~150 MB | ⚡ Fastest | ⭐ Low | Quick notes, testing |
| `base` | ~300 MB | ⚡ Fast | ⭐⭐ Good | General use on older Macs |
| `small` | ~1 GB | ⚡ Moderate | ⭐⭐⭐ Better | **Recommended** — Best balance |
| `medium` | ~3 GB | 🐌 Slower | ⭐⭐⭐⭐ High | Accuracy-critical tasks |
| `large-v3` | ~6 GB | 🐌 Slowest | ⭐⭐⭐⭐⭐ Highest | Maximum accuracy, powerful hardware |

### All Configuration Options

| Variable | Default | Options | Description |
|----------|---------|---------|-------------|
| `ASR_ENGINE` | `local` | `local`, `openai_api` | Use local Whisper or OpenAI API |
| `WHISPER_MODEL` | `small` | `tiny`, `base`, `small`, `medium`, `large-v3` | Model size (see table above) |
| `WHISPER_LANGUAGE` | `en` | ISO 639-1 codes | Language for transcription |
| `HOTKEY_MODE` | `toggle` | `toggle`, `hold` | Recording mode |
| `TEXT_PROCESSOR` | `regex` | `regex`, `ollama` | Text cleanup method |
| `SAMPLE_RATE` | `16000` | Hz | Audio sample rate |
| `ENABLE_SOUND_FEEDBACK` | `false` | `true`, `false` | Play beeps on start/stop |
| `SHOW_PREVIEW_NOTIFICATION` | `false` | `true`, `false` | Show transcription before pasting |
| `OPENAI_API_KEY` | — | Your API key | Required if `ASR_ENGINE=openai_api` |

---

## 🛠️ Troubleshooting

### "Dictate only runs on macOS"
This app uses macOS-specific APIs (rumps, pyobjc) and is designed for macOS only.

### Hotkey doesn't work
1. Check **System Settings → Privacy & Security → Accessibility**
2. Make sure your terminal app is in the list and enabled
3. Try removing and re-adding it
4. Restart the terminal app after granting permissions

### No audio recorded / silent transcription
1. Check microphone permission in **System Settings → Privacy & Security → Microphone**
2. Make sure your microphone is set as the default input device
3. Check the logs for errors: `python -m dictate` will show debug output

### "Text injected" but nothing appears
- The app pastes text using Cmd+V, so make sure:
  - You have a text field focused (cursor blinking)
  - The app supports clipboard paste
  - Try clicking into a text field before recording

### Transcription is very slow
- Try a smaller model: Change `WHISPER_MODEL=base` or `tiny` in `.env`
- Check CPU usage during transcription
- The first transcription loads the model (one-time delay)

### Wrong language detected
- Set `WHISPER_LANGUAGE=en` (or your language code) in `.env`
- Force language prevents Whisper from auto-detecting incorrectly

### App crashes on startup
```bash
# Reinstall dependencies
source .venv/bin/activate
pip install --force-reinstall -e .

# Check Python version (requires 3.10-3.13)
python --version
```

---

## 🤖 Auto-Start on Login

To run Dictate automatically when you log in:

1. Edit `scripts/com.dictate.app.plist`:
   - Update the Python path to your virtual environment
   - Update the working directory path

2. Install the launch agent:
   ```bash
   cp scripts/com.dictate.app.plist ~/Library/LaunchAgents/
   launchctl load ~/Library/LaunchAgents/com.dictate.app.plist
   ```

3. Verify it's running:
   ```bash
   launchctl list | grep dictate
   ```

To stop auto-start:
```bash
launchctl unload ~/Library/LaunchAgents/com.dictate.app.plist
rm ~/Library/LaunchAgents/com.dictate.app.plist
```

---

## 🏗️ Architecture

```
src/dictate/
├── app.py                  # Menu bar UI (rumps)
├── pipeline.py             # Orchestrator: audio → ASR → cleanup → paste
├── config.py               # Configuration loader (.env)
├── audio/
│   ├── recorder.py         # Microphone recording (sounddevice)
│   └── sound_feedback.py   # Beep sounds for start/stop
├── asr/
│   ├── whisper_local.py    # Local Whisper transcription
│   └── whisper_api.py      # OpenAI API fallback
├── processing/
│   ├── regex_processor.py  # Filler removal + punctuation
│   └── ollama_processor.py # LLM-based cleanup (stub)
├── hotkey/
│   ├── pynput_listener.py  # Global hotkey (pynput)
│   └── pyobjc_fn_listener.py # Alternative implementation
├── injection/
│   └── injector.py         # Clipboard + Cmd+V paste
└── notification/
    └── notifier.py         # macOS notifications
```

Each component uses Protocol interfaces + factory pattern for easy swapping and testing.

---

## 🧪 Development

### Running Tests

```bash
source .venv/bin/activate
pip install -e ".[dev]"
pytest tests/ -v
```

### Code Structure

- **Modular design** — Each component (ASR, processor, hotkey, etc.) is swappable
- **Protocol-based** — All interfaces use Python Protocols for type safety
- **Factory pattern** — Components are created via factory functions based on config
- **Fully tested** — 29 unit tests covering core functionality

### Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📋 Requirements

- **macOS 12+** (Monterey or later)
- **Python 3.10–3.13** — **Use Python 3.12 for best compatibility**
  - ⚠️ Python 3.14 is NOT supported (faster-whisper lacks 3.14 wheels)
  - If you have Python 3.14, install Python 3.12: `brew install python@3.12`
- **~1 GB RAM** for the `small` model
- **~500 MB disk space** for model download

---

## 🔮 Roadmap

- [x] Toggle and hold-to-talk modes
- [x] Sound feedback
- [x] Preview notifications
- [ ] Ollama/LLM-based text processing for better grammar
- [ ] Transcription history log
- [ ] Per-app cleanup profiles
- [ ] System-wide settings UI
- [ ] Code dictation mode (no filler removal)

---

## 📄 License

MIT License — See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- **Inspiration**: [Wispr Flow](https://wisprflow.com)
- **ASR**: [faster-whisper](https://github.com/SYSTRAN/faster-whisper) by SYSTRAN
- **Whisper**: [OpenAI Whisper](https://github.com/openai/whisper)

---

## 💬 Support

- **Issues**: [GitHub Issues](https://github.com/ADJ-HUB1/dictate/issues)
- **Questions**: Check [Troubleshooting](#-troubleshooting) first
- **Feature Requests**: Open an issue with the "enhancement" label

---

**Made with ❤️ for privacy-conscious Mac users who want fast, offline dictation.**
