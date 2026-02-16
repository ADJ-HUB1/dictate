# Dictate — Development Progress

## Current State: Working MVP

The app is functional. Press Option+Space to toggle recording, speak, press Option+Space again — cleaned text is pasted into the focused app. Running on Python 3.12 venv alongside system Python 3.14.

---

## Session 1 — Initial Build & Tuning

### What We Built
- Full project structure: 39 files across 9 modules
- Menu bar app (rumps) with idle/recording/processing icon states
- Audio recording via sounddevice → numpy arrays
- ASR via faster-whisper (local) with OpenAI API fallback
- Regex-based filler word removal + punctuation insertion
- Hotkey listener (Option+Space via pynput)
- Text injection via clipboard + Cmd+V
- Pipeline orchestrator connecting all components
- 29 unit tests — all passing
- Python 3.12 venv (via Homebrew) to avoid conflicts with system Python 3.14

### Models Tested

| Model | Size | Speed (27s audio) | Accuracy | Issues |
|-------|------|-------------------|----------|--------|
| `tiny` | ~75 MB | ~1-2s | Low | Fast but mishears many words |
| `base` | ~150 MB | ~4s | Medium | "fill" → "feel", "input" → "imputes", poor punctuation |
| `small` | ~1 GB | ~3s (int8) / ~57s (float32) | Good | Best balance. Still mishears some words ("inputs" → "imputes") |

### Issues Detected & Fixed

1. **Wrong language detection (Critical)**
   - Whisper auto-detected "yo" (Yoruba) and transcribed in Telugu script
   - Fix: Force `language="en"` in transcribe call
   - File: `src/dictate/asr/whisper_local.py`

2. **Extremely slow transcription (~57s for 21s audio)**
   - Cause: `compute_type="auto"` defaulted to float32 on CPU, `beam_size=5`
   - Fix: Changed to `compute_type="int8"`, `beam_size=3`, added `vad_filter=True`
   - File: `src/dictate/asr/whisper_local.py`

3. **No punctuation in output**
   - Cause: Whisper base/small models don't always add punctuation
   - Fix: Added `initial_prompt` to prime Whisper for punctuated English output
   - File: `src/dictate/asr/whisper_local.py`

4. **"So ," comma artifact**
   - Cause: Comma-before-conjunction regex fired on short words at sentence starts
   - Fix: Changed lookbehind to require 3+ lowercase chars before inserting comma
   - File: `src/dictate/processing/regex_processor.py`

5. **pyproject.toml build backend error**
   - Cause: `setuptools.backends._legacy:_Backend` doesn't exist in modern setuptools
   - Fix: Changed to `setuptools.build_meta`

6. **Python 3.14 incompatibility**
   - faster-whisper and several deps don't have 3.14 wheels
   - Fix: `brew install python@3.12`, created dedicated `.venv` with 3.12
   - System Python 3.14 is untouched

### Current Settings (.env)
```
ASR_ENGINE=local
WHISPER_MODEL=small
WHISPER_LANGUAGE=en
TEXT_PROCESSOR=regex
HOTKEY_BACKEND=pynput
SAMPLE_RATE=16000
```

---

## Known Issues (To Fix)

### Accuracy
- [ ] "inputs" transcribed as "imputes" — `small` model limitation
- [ ] Some words still mishear in fast speech
- [ ] `medium` model (~3 GB) would improve accuracy — need to test speed with int8

### Formatting
- [ ] ", So" and ", And" — capitals appearing after commas mid-sentence
- [ ] Comma insertion logic is basic — doesn't handle all clause patterns
- [ ] No smart sentence boundary detection

### Filler Removal
- [ ] Some fillers removed too aggressively in certain contexts
- [ ] "basically" removed even when used meaningfully
- [ ] Need context-aware filler detection (future: Ollama processor)

---

## Feature Requests (Future)

### Hold-to-Talk Mode (Priority)
- **How it works**: Hold a key → recording starts → release key → recording stops, transcribes, and injects
- **Current**: Toggle mode only (Option+Space to start, Option+Space to stop)
- **Implementation plan**:
  - Add a new hotkey listener mode: "hold" vs "toggle"
  - On key press → start recording
  - On key release → stop recording + process
  - Config: `HOTKEY_MODE=toggle` or `HOTKEY_MODE=hold`
  - Key candidate: could use a modifier key (e.g., Right Option, Right Command) or a function key
  - Note: Fn key is intercepted by macOS for emoji picker — unreliable
  - pynput supports `on_press` / `on_release` events which makes this straightforward

### Ollama/LLM Post-Processing
- Replace regex processor with local LLM cleanup via Ollama
- Would fix grammar, punctuation, and word corrections in one pass
- Stub already exists at `src/dictate/processing/ollama_processor.py`

### Other Ideas
- [ ] Sound feedback (beep on start/stop recording)
- [ ] Show transcribed text in a notification before injecting
- [ ] Per-app profiles (different cleanup rules for email vs code comments)
- [ ] Transcription history log

---

## How to Resume Development

```bash
cd ~/Documents/ClaudeCode/My_personal_project/dictate
source .venv/bin/activate
python -m pytest tests/ -v    # Verify everything works
python -m dictate              # Run the app
```

### Key Files to Know
| File | Purpose |
|------|---------|
| `src/dictate/asr/whisper_local.py` | Whisper settings (model, int8, beam size, language, initial_prompt) |
| `src/dictate/processing/regex_processor.py` | Filler removal + punctuation rules |
| `src/dictate/hotkey/pynput_listener.py` | Hotkey binding (where hold-to-talk would go) |
| `src/dictate/pipeline.py` | Orchestrator — connects recording → ASR → cleanup → paste |
| `src/dictate/config.py` | All config options and validation |
| `.env` | Runtime settings |
