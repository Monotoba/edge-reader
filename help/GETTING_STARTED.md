# Getting Started with Edge Reader

Edge Reader is a cross-platform desktop application that reads documents aloud using text-to-speech technology. It supports numerous document formats and can generate offline audio bundles for playback without internet.

## Installation

Edge Reader requires Python 3.10 or later and PySide6. Install the package:

```bash
pip install edge-readaloud-pyside6
```

Or for development:

```bash
git clone <repository>
cd DocReader
pip install -e ".[dev]"
```

## First Steps

1. **Launch the application** — Run `edge-reader` from the command line or open the Edge Reader application.

2. **Open a document** — Click "Open Document" or use File → Open Document to load a supported file:
   - Text formats: TXT, Markdown, RST, CSV, JSON, XML, YAML
   - Web formats: HTML, XHTML
   - E-books: EPUB, PDF, DOCX, RTF
   - With Calibre: MOBI, AZW, AZW3, FB2, LIT, PDB

3. **Choose a voice** — Select your preferred language and voice from the dropdowns. Click "Refresh Voices" to download the latest available voices from Microsoft.

4. **Adjust settings** (optional) — Set TTS speed with the rate slider (-90% to +200% normal speed).

5. **Click "Play"** — Start listening immediately! Audio synthesizes on-the-fly as each sentence plays (requires internet). The current sentence is highlighted in yellow. Use the playback controls:
   - **Play** — Start from the beginning or resume
   - **Pause** — Pause the current playback
   - **Stop** — Stop and reset to the beginning
   - **Volume** — Adjust playback volume with the slider

## Optional: Generate an Offline Bundle

To save a document for offline playback (flights, travel, no wifi):

1. Open a document and configure voice/speed (see steps 2-4 above)
2. Click **"Generate Offline Bundle"** to create a `.edgevoice.zip` file
3. Choose a save location and wait for synthesis to complete
4. Later, click **File → Open Offline Bundle** to play without internet

The bundle contains:
   - Pre-synthesized MP3 audio for each sentence
   - Timing information for word-level synchronization (future feature)
   - Full document text for highlighting during playback
   - Manifest with metadata

## Common Workflows

### Quick listening (live mode — recommended for one-time reads)
1. Open a document
2. Choose voice and settings
3. Click "Play" — starts immediately with live synthesis
4. Adjust volume as needed

### Offline playback (for long-term use, travel, etc.)
1. Open a document
2. Configure voice/speed
3. Click "Generate Offline Bundle" and save the `.edgevoice.zip` file
4. Open the bundle anytime later with File → Open Offline Bundle
5. Play without internet — perfect for flights and travel

### Batch processing (listen once, save for later)
1. Open a document and click "Play" to listen (live mode)
2. While reading, click "Generate Offline Bundle" to save it
3. You can listen again offline anytime without re-synthesizing

### Using with different languages
The voice list updates automatically when you change the language dropdown. Microsoft's edge-tts provides voices for numerous languages and locales.

## Tips & Tricks

- **Live playback requires internet** — Each sentence synthesizes on-the-fly. If your connection drops, synthesis fails and you'll see an error.
- **Bundles are completely offline** — Once generated, bundles are self-contained and work without any internet connection.
- **Large documents** — Documents are automatically split into manageable chunks. Very long books may take several minutes to generate into a bundle.
- **Live is fast, bundles are reliable** — Use live mode for quick reads; use bundles for critical playback (presentations, travel) where network isn't available.
- **Detailed error logs** — If synthesis fails, check the detailed error information to diagnose issues.

## Supported Audio Formats

Generated bundles use MP3 audio. Playback requires Qt multimedia support (included with PySide6).

## Getting Help

- See [USER_MANUAL.md](USER_MANUAL.md) for detailed feature documentation
- See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues and solutions
