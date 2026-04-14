# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the tool

```shell
# Run with interactive shell menu (no args)
python -m transcripy

# Run with specific command
python -m transcripy --audio-to-text --model medium --language english
python -m transcripy --audio-to-voices
python -m transcripy --text-to-splits
python -m transcripy --transcribe
python -m transcripy --set-speakers
python -m transcripy --map-speakers --threshold 0.2
python -m transcripy --slice --pre 0.1 --post 0.2
python -m transcripy --viewer
python -m transcripy --create-dataset <SPEAKER>
python -m transcripy --audio-extract-voice --model spleeter:2stems
```

Common flags: `--data-path <path>` (default: `./data`), `--verbose`

## Architecture

The package entry point (`__main__.py`) dispatches to either `shellMenu.py` (interactive TUI, no args) or `cli.py` (argparse CLI).

**Processing pipeline** (each step produces input for the next):

1. **`audioPreprocessing.py`** — voice extraction via Spleeter: `raw_audio/` → `raw_audio_voices/`
2. **`audio2text.py`** — Whisper ASR: `raw_audio_voices/*.wav` → `text/*.json` (segments with timestamps)
3. **`audio2voices.py`** — Pyannote diarization: `raw_audio_voices/*.wav` → `diarization/*.rttm`
4. **`setSpeakers.py`** / **`mapSpeakers.py`** — rename/map speaker IDs in `.rttm` files, stored as sidecar `.json` overwrite files
5. **`text2splits.py`** — joins text segments with diarization to produce `voice_splits/*.json` (per-speaker segments); also handles `--transcribe` output to `output/transcripts/`
6. **`sliceAudio.py`** — cuts audio per segment → `output/slices/`
7. **`createDataset.py`** — builds TTS training dataset from a named speaker
8. **`viewer.py`** — generates HTML analysis in `output/analysis/`

**Core base class:** `helper.MultiFileHandler` — all multi-file processors extend this. It scans input dir, skips existing outputs (unless `ignore_existing=True`), and calls `handler(input_file, output_file, idx)` per file.

**Data formats:**
- Diarization: RTTM format (`.rttm`) with optional speaker rename sidecar (`.json`)
- Text: Whisper JSON with `{segments, language, text}` keys
- Splits: JSON dict keyed by speaker name → list of `{start, end, text}` segments

`helper.read_rttm()` automatically applies speaker renames from the sidecar `.json` when loading RTTM files.
