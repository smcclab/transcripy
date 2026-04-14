# Design: Poetry Install & Simplified README

**Date:** 2026-04-14  
**Scope:** Add Poetry packaging, rewrite README for macOS-focused multi-speaker transcription workflow. Drop voice synthesis. No per-OS alternatives.

---

## Goal

Make it straightforward for a macOS user to go from a `.wav` audio file to a multi-speaker transcription using local hardware. The install should be a single `poetry install` command after minimal system setup.

---

## 1. `pyproject.toml`

Create a new `pyproject.toml` at the repo root using Poetry's standard format.

**Project metadata:**
- Name: `transcripy`
- Python: `^3.12`
- Description: Local multi-speaker audio transcription

**CLI entry point:**
```
[tool.poetry.scripts]
transcripy = "transcripy.cli:main"
```
This lets users run `transcripy` instead of `python -m transcripy`.

**Dependencies:**

| Package | Notes |
|---|---|
| `openai-whisper` | ASR — installed via git source since not stable on PyPI |
| `pyannote.audio` | Speaker diarization |
| `spleeter` | Voice extraction (optional first step) |
| `tensorflow = "2.20.*"` | Required by spleeter; pinned for stability |
| `tqdm` | Progress bars |
| `pydub` | Audio manipulation |
| `plotly` | Viewer HTML output |
| `mutagen` | Audio metadata |
| `simpleaudio` | Audio playback |
| `pycaption` | Transcript format output |
| `simple-term-menu` | Interactive TUI menu |
| `colour` | Colour utilities |

`ffmpeg` remains a system dependency installed via Homebrew — not managed by Poetry.

No optional extras groups. All deps are required. Spleeter/TF are included because they're part of the documented pipeline; users who skip voice extraction still benefit from having a complete install.

---

## 2. README Rewrite

**Remove entirely:**
- Linux/Windows install instructions
- Per-step "follow setup instructions from [X]" redirections
- Alternatives sections (RipX, Voice-Cloning-App, Real-Time Voice Cloning)
- Voice synthesis section and submodule reference
- Jupyter notebook "Related" link
- Per-step optional arguments reference (covered by `transcripy --help`)

**New structure:**

### What it does
2–3 sentences: local multi-speaker transcription from `.wav` audio using Whisper (ASR), Pyannote (speaker diarization), and optionally Spleeter (voice extraction). Runs entirely on local hardware.

### Requirements
- macOS with [Homebrew](https://brew.sh)
- `brew install ffmpeg`
- [Poetry](https://python-poetry.org/docs/#installation)

### Install
```shell
git clone <repo>
cd transcripy
poetry install
```

### HuggingFace setup
Pyannote downloads its models from HuggingFace and requires a free account with model access accepted. One-time setup:
1. Create account at huggingface.co
2. Accept terms for `pyannote/speaker-diarization` and `pyannote/segmentation` models
3. Run `huggingface-cli login`

Link: https://huggingface.co/pyannote/speaker-diarization

### Data layout
```
data/
    raw_audio_voices/    # Place your .wav files here
    diarization/         # Generated
    text/                # Generated
    output/transcripts/  # Final output
```

### Quick start
```shell
# Optional: extract voice from audio with background noise
transcripy --audio-extract-voice

# Transcribe audio to text
transcripy --audio-to-text --model medium --language english

# Detect speakers
transcripy --audio-to-voices

# Combine into transcription
transcripy --transcribe
```

### Options
| Flag | Default | Description |
|---|---|---|
| `--data-path` | `./data` | Root data directory |
| `--model` | varies | Whisper model size (tiny/base/small/medium/large) |
| `--language` | auto-detect | Force language for transcription |
| `--verbose` | off | Print debug output |

---

## 3. Removed Features

**Voice synthesis** (`--voice-synthesis`, `synthesizer.py`, `tools/voiceSynthesizer` submodule): not documented, not included in Poetry deps. Code is kept but unsupported. The git submodule remains but is not referenced in the README.

---

## Out of Scope

- Refactoring processing code
- Adding tests
- Windows/Linux support
- Optional extras groups for spleeter
