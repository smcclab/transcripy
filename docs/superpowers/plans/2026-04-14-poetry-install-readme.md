# Poetry Install & README Rewrite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `pyproject.toml` for Poetry-based install and rewrite `README.md` for a clean macOS-focused path from `.wav` to multi-speaker transcription.

**Architecture:** Create `pyproject.toml` at repo root declaring all runtime dependencies (derived from actual source imports, not the old README). Rewrite `README.md` from scratch — no Linux/Windows, no alternatives, no per-step external setup links. Verify with `poetry check`.

**Tech Stack:** Poetry, Python ^3.12, openai-whisper (git), pyannote.audio, spleeter, tensorflow 2.20.x

---

## File Map

| File | Action | Notes |
|---|---|---|
| `pyproject.toml` | Create | New Poetry config at repo root |
| `README.md` | Rewrite | Simplified macOS-only docs |

---

### Task 1: Create `pyproject.toml`

**Files:**
- Create: `pyproject.toml`

- [ ] **Step 1: Write `pyproject.toml`**

Create `/Users/charles/src/transcripy/pyproject.toml` with this exact content:

```toml
[tool.poetry]
name = "transcripy"
version = "0.1.0"
description = "Local multi-speaker audio transcription"
authors = ["Charles Martin"]
readme = "README.md"
packages = [{include = "transcripy"}]

[tool.poetry.dependencies]
python = "^3.12"
openai-whisper = {git = "https://github.com/openai/whisper.git"}
"pyannote.audio" = "*"
spleeter = "*"
tensorflow = "~2.20"
tqdm = "*"
pydub = "*"
plotly = "*"
mutagen = "*"
pycaption = "*"
colour = "*"
colorama = "*"
numpy = "*"
scipy = "*"
console-menu = "*"

[tool.poetry.scripts]
transcripy = "transcripy.cli:main"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

- [ ] **Step 2: Verify the file is valid**

```bash
cd /Users/charles/src/transcripy && poetry check
```

Expected output: `All set!` (or similar — no errors). If Poetry reports an unknown package or syntax error, fix the offending line.

- [ ] **Step 3: Commit**

```bash
git add pyproject.toml
git commit -m "feat: add pyproject.toml for Poetry install"
```

---

### Task 2: Rewrite `README.md`

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Replace `README.md` with the new content**

Overwrite `/Users/charles/src/transcripy/README.md` with:

````markdown
# transcripy

Local multi-speaker audio transcription. Takes `.wav` audio and produces speaker-labelled transcripts using [OpenAI Whisper](https://github.com/openai/whisper) for speech recognition and [Pyannote](https://github.com/pyannote/pyannote-audio) for speaker diarization. Runs entirely on local hardware.

---

## Requirements

- macOS with [Homebrew](https://brew.sh)
- [Poetry](https://python-poetry.org/docs/#installation)

Install system dependency:

```shell
brew install ffmpeg
```

---

## Install

```shell
git clone <repo-url>
cd transcripy
poetry install
```

---

## HuggingFace setup

Pyannote downloads its speaker diarization models from HuggingFace and requires a free account with model access accepted before first use.

1. Create a free account at [huggingface.co](https://huggingface.co)
2. Accept the model terms at [pyannote/speaker-diarization](https://huggingface.co/pyannote/speaker-diarization) and [pyannote/segmentation](https://huggingface.co/pyannote/segmentation)
3. Log in via the CLI:

```shell
poetry run huggingface-cli login
```

---

## Data layout

Place your `.wav` files in `data/raw_audio_voices/` before running. All output is written under `data/`.

```
data/
    raw_audio_voices/    # Your input .wav files go here
    text/                # Whisper transcription output
    diarization/         # Speaker diarization output
    output/
        transcripts/     # Final transcripts
        slices/          # Per-speaker audio slices
        analysis/        # HTML viewer output
```

---

## Quick start

Run each step in order. All commands use `poetry run transcripy` (or activate the virtualenv with `poetry shell` first).

```shell
# Optional: extract voice track from audio with background noise/music
# Skip this if your audio is already clean speech
poetry run transcripy --audio-extract-voice

# Transcribe audio to text using Whisper
poetry run transcripy --audio-to-text --model medium --language english

# Detect and label individual speakers
poetry run transcripy --audio-to-voices

# Combine transcription and speaker labels into output transcripts
poetry run transcripy --transcribe
```

---

## Options

| Flag | Default | Description |
|---|---|---|
| `--data-path <path>` | `./data` | Root data directory |
| `--model <name>` | varies per step | Whisper model: `tiny` `base` `small` `medium` `large` |
| `--language <lang>` | auto-detect | Force language for `--audio-to-text` |
| `--verbose` | off | Print debug output |

Run `poetry run transcripy --help` for the full list.

---

## Interactive menu

Running without arguments opens an interactive menu:

```shell
poetry run transcripy
```
````

- [ ] **Step 2: Review the rendered output**

Read the file back and confirm it looks clean with no leftover sections from the old README.

```bash
cat /Users/charles/src/transcripy/README.md
```

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs: rewrite README for macOS Poetry install"
```
