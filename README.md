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
