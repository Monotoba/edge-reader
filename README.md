# Edge Reader — PySide6 + edge-tts

A cross-platform desktop read-aloud application that loads text/document/ebook files and reads them aloud using Microsoft Edge online neural TTS through `edge-tts`. Play documents immediately with live synthesis (internet required), or generate a self-contained offline replay bundle for later offline playback. Highlights each sentence while reading.

## Important status note

`edge-tts` uses Microsoft's Edge online TTS service, but it is not an official Microsoft API. It is suitable for personal tools and experiments, but production/commercial/distributed products should evaluate Azure AI Speech or another supported TTS provider.

## Features

- PySide6 desktop GUI.
- Load common text/document formats:
  - TXT, Markdown, RST, CSV, JSON, XML, YAML
  - HTML/XHTML
  - EPUB
  - PDF
  - DOCX
  - RTF
  - Optional MOBI/AZW/AZW3/FB2/LIT/PDB through Calibre's `ebook-convert` command.
- Language and voice selector.
- TTS speed setting using the `edge-tts` rate parameter.
- Volume control.
- **Sentence-by-sentence highlighting** during playback (yellow background).
- **Word-level highlighting** option for real-time word tracking (cyan background, bold).
- **Live playback:** Play documents immediately with on-the-fly audio synthesis (requires internet).
- **Offline bundles:** Generate `.edgevoice.zip` files for later playback without internet access. Bundles contain:
  - `document.txt`
  - `manifest.json`
  - `timings.json`
  - one MP3 audio segment per sentence/chunk
- Stores edge-tts word/sentence boundary events per segment for future word-highlighting or subtitle export.

## Design choice: one MP3 per sentence

Long documents and ebooks can exceed TTS service message limits and make global timestamp alignment fragile. This app synthesizes each sentence/chunk as a separate MP3 segment. Playback advances segment-by-segment, so sentence highlighting remains exact and offline replay is simple. The raw API boundary events are still stored in the bundle for later word-level synchronization work.

## Install on Linux/macOS/Windows

Python 3.10 or newer is recommended.

```bash
python3 -m venv .venv
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\activate        # Windows PowerShell/cmd equivalent

python -m pip install --upgrade pip
pip install -e ".[dev]"
```

Run the app:

```bash
python -m edge_reader
# or, after editable install:
edge-reader
```

Run tests:

```bash
pytest
```

Recommended local Git workflow:

```bash
git init
git add .
git commit -m "Initial PySide6 edge-tts read-aloud app"
```

## Linux multimedia notes

QtMultimedia uses platform audio/video backends. If MP3 playback fails on Ubuntu or another Linux distribution, install the system multimedia plugins. On Ubuntu, this is often enough:

```bash
sudo apt install gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
                 gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly
```

If PySide6 fails to start on some minimal Linux installs, also install common Qt/XCB support packages such as `libxcb-cursor0`.

## Optional Calibre bridge for MOBI/AZW3/etc.

The app directly supports EPUB. MOBI/AZW/AZW3 and related ebook formats are handled by Calibre if `ebook-convert` is available in your PATH.

Install Calibre from your OS package manager or from the official Calibre project, then verify:

```bash
ebook-convert --version
```

## Basic use

### Live playback (immediate, requires internet):

1. Click **Open Document** and select a file.
2. Choose a language and voice.
3. Set TTS speed (optional).
4. Click **Play**.

Audio synthesizes on-the-fly as each sentence plays. This is the fastest way to start listening.

### Offline playback (generate bundle for later):

1. Complete the steps above to load and configure a document.
2. Click **Generate Offline Bundle** (requires internet).
3. Save the `.edgevoice.zip` bundle to your computer.
4. Later, click **Open Bundle** and choose the saved file to play without internet.

Playback and sentence highlighting work offline without regenerating audio.

## Live vs. offline playback

**Live mode** (default):
- Play immediately after opening a document
- Audio synthesizes sentence-by-sentence as you listen
- Requires internet connection (one sentence at a time)
- No pre-generation delay; start listening in seconds
- Status bar shows "(live)" during playback

**Offline mode**:
- Generate a bundle once, play anytime without internet
- Bundle creation takes time (depends on document length)
- Once bundled, playback is instant and does not require network
- Status bar shows "(offline)" during playback
- Ideal for long documents, flights, travel, or spotty connectivity

The playback experience is identical in both modes: sentence highlighting, pause/resume, volume control, and progress tracking all work the same way.

## Bundle format

A bundle is a zip file with this structure:

```text
manifest.json
document.txt
timings.json
audio/000000.mp3
audio/000001.mp3
...
```

Current schema:

- `manifest.json` describes the source, voice, language, TTS rate, sentence spans, and audio file names.
- `timings.json` stores edge-tts `WordBoundary` and `SentenceBoundary` events in milliseconds for each segment.
- `document.txt` stores the extracted plain text used by the reader.
- `audio/*.mp3` stores sentence/chunk-level audio.

## Development notes

The project keeps GUI and non-GUI logic separated so parsing and bundle behavior can be tested without requiring a display server or network connection.

Useful files:

- `src/edge_reader/main.py` — PySide6 GUI, playback logic, and live/offline mode branching.
- `src/edge_reader/workers.py` — `SynthesisWorker` (bundle generation), `VoiceListWorker` (voice fetch), `LivePlaybackWorker` (on-demand sentence synthesis).
- `src/edge_reader/document.py` — file/document extraction.
- `src/edge_reader/textseg.py` — sentence/chunk splitting with offsets.
- `src/edge_reader/tts_edge.py` — edge-tts synthesis primitives and boundary capture.
- `src/edge_reader/bundle.py` — offline bundle creation/loading/unpacking.
- `tests/` — unit tests for parser/rate/bundle logic.

## Word-Level Highlighting

Enable the "Word-level Highlight" checkbox in the toolbar to see individual words highlighted in cyan (with bold text) as they're spoken during playback. This feature uses the timing data captured from the edge-tts API for precise word synchronization.

**Note:** Word-level highlighting requires an offline bundle; it does not work with live playback mode (as boundary events are only captured during bundle generation).

## Known limitations

- `edge-tts` is unofficial and can change or break independently of this app.
- Generating large books can take a long time because each sentence/chunk is synthesized separately.
- PDF extraction quality depends on the source PDF. Scanned PDFs require OCR before this app can read them.
- Sentence splitting is heuristic. It works well for ordinary prose but will not be perfect for every technical document, screenplay, OCR artifact, or legal citation.
- Word-level highlighting is available in offline bundle mode only; live playback mode does not capture word boundary events.
