# Edge Reader User Manual

This manual provides comprehensive documentation for all features of Edge Reader.

## Table of Contents

1. [Main Interface](#main-interface)
2. [Opening Documents](#opening-documents)
3. [Voice Selection](#voice-selection)
4. [Playback Controls](#playback-controls)
5. [Offline Bundles](#offline-bundles)
6. [Keyboard Shortcuts](#keyboard-shortcuts)
7. [Settings & Preferences](#settings--preferences)
8. [File Formats](#file-formats)

## Main Interface

The Edge Reader window consists of:

- **Toolbar** (top) — Quick access to core functions: Open Document, Open Bundle, language/voice selectors, rate control, and generation button
- **Text Display Area** (center) — Shows the full document text with current sentence highlighted in yellow during playback
- **Playback Controls** (bottom) — Play, Pause, Stop buttons, volume slider, and progress bar

### Status Bar

The status bar at the bottom shows:
- Current operation status (loading, generating, playing, etc.)
- Document info (number of sentences/chunks)
- Progress information

## Opening Documents

### Via "Open Document" Button

1. Click "Open Document" in the toolbar or select File → Open Document
2. Browse to your document and click "Open"
3. If successful, the document text appears in the main display area and the status bar shows the sentence count

### Supported Formats

**Text Files:**
- Plain text (.txt)
- Markdown (.md, .markdown)
- reStructuredText (.rst)
- CSV, JSON, XML, YAML files (displayed as-is, no special parsing)

**Web Content:**
- HTML (.html, .htm, .xhtml) — scripts and styles removed, text extracted

**E-Books:**
- EPUB (.epub)
- PDF (.pdf) — requires PyMuPDF
- DOCX (.docx) — Microsoft Word documents
- RTF (.rtf) — Rich Text Format
- MOBI, AZW, AZW3, FB2 (.mobi, .azw, .azw3, .fb2) — requires Calibre's `ebook-convert` command in PATH

### Error Messages

If a document fails to load, check:
- File exists and is readable
- File extension is supported
- For MOBI/AZW files, Calibre is installed: `which ebook-convert`
- PDF/EPUB dependency is installed: `pip install PyMuPDF ebooklib`

## Voice Selection

### Language Dropdown

Displays all available languages/locales. Selecting a language filters the voice list to show only voices for that language.

### Voice Dropdown

Shows voices available for the selected language. Voices typically indicate:
- Gender (if available)
- Display name or description

Your last selected language and voice are saved and restored on next launch.

### "Refresh Voices" Button

Downloads the latest available voices from Microsoft edge-tts. This requires internet access. The operation may take a few seconds.

**Note:** If voice refresh fails, Edge Reader falls back to a built-in list of common voices. Check your internet connection and try again.

## Navigating the Document

### Document Navigator Panel

The **Document Navigator** panel appears on the left side of the window and shows all paragraphs in the document. Each entry displays:
- A paragraph number (¶)
- A preview of the first 60 characters

**To jump to a paragraph:** Click any entry in the navigator list. The document will jump to that paragraph immediately.

**To show/hide the navigator:** Go to View menu and toggle "Document Navigator", or click the X on the panel to hide it and the button to show it again.

### Jumping to a Specific Location

You can also **double-click any text in the document** directly to jump to that sentence. This is useful for:
- Skipping legal text, disclaimers, or introductions
- Jumping past table of contents or indexes
- Skipping to a specific chapter or section
- Going back to re-listen to something

When you double-click or click a navigator entry:
1. The document jumps to that location
2. The location is highlighted in yellow
3. Progress updates to show your new position
4. Click Play to start reading from that location

**Note:** Jumping does not start playback automatically—use Play to start listening from the new position.

## Playback Controls

### Play Button

Starts playback from the beginning of the document, from a jumped position, or resumes after pause.

**Two playback modes:**

1. **Live mode** (default) — Audio synthesizes on-the-fly as you listen
   - Enabled immediately after opening a document
   - Requires internet connection (one sentence at a time)
   - Playback starts in 1-2 seconds
   - Status bar shows "(live)"

2. **Offline mode** — Audio plays from a pre-generated bundle
   - Enabled after opening a `.edgevoice.zip` bundle
   - No internet required
   - Instant playback (no synthesis delay)
   - Status bar shows "(offline)"

### Pause Button

Temporarily pauses playback. Click Play to resume from the same position.

### Stop Button

Completely stops playback and resets to the beginning. Progress bar returns to 0. Temporary live audio files are cleaned up.

### Volume Slider

Controls playback volume from 0% (mute) to 100%. Your volume preference is saved between sessions.

### Progress Bar

Shows:
- Current progress as a percentage
- Current sentence number / total sentences (e.g., "Reading 15/147")

The progress bar fills as playback progresses through sentences.

### Word-Level Highlighting

Check the "Word-level Highlight" checkbox in the toolbar to enable real-time word highlighting during playback.

**How it works:**
- As each word is spoken, it is highlighted with a cyan background and bold text
- The highlighting moves word-by-word through the document in sync with audio
- Requires an offline bundle (boundary event data is captured during generation)
- Does not work with live playback mode

**When to use:**
- Language learning or pronunciation practice
- Helping readers with attention/tracking difficulties
- Accessibility for some users
- Analyzing word-level timing in the audio

**Limitation:** Live playback mode does not capture word boundary data, so word-level highlighting is only available when playing from an offline bundle.

## Offline Bundles (Optional)

An offline bundle (`.edgevoice.zip` file) contains pre-synthesized audio for a document, enabling playback without internet. Bundles are optional — you can start listening immediately with live mode.

**When to create a bundle:**
- You want to listen offline (flights, travel, no wifi)
- You want to share the audio with someone else
- You want to avoid synthesis delays for repeated playback
- You want a permanent audio backup of a document

**Bundle contents:**
- Pre-synthesized MP3 audio for every sentence
- Complete document text
- Timing/synchronization data
- Metadata (voice, language, rate, title, source)

### Generating a Bundle

1. Open a document
2. Choose language and voice
3. Optionally adjust playback rate with the TTS speed slider
4. Click "Generate Offline Bundle"
5. Choose a location and filename for the `.edgevoice.zip` file
6. Click "Save"

You can generate a bundle while listening (live mode) — it doesn't interrupt playback.

The generation process:
- Connects to the Microsoft edge-tts API (requires internet)
- Synthesizes audio for each sentence
- Shows progress in the status bar
- Displays a progress bar as sentences are processed

**Duration:** Depends on document length. Typical speed is 30-60 seconds per 1000 words.

### Opening a Bundle

1. Click "Open Bundle" or select File → Open Offline Bundle
2. Browse to a `.edgevoice.zip` file
3. Click "Open"

The bundle is extracted to a temporary directory. Previous bundles are automatically cleaned up.

### Error Handling During Generation

If generation fails:
1. A dialog appears with an error message
2. Click "Details" to see the full error traceback
3. Common issues:
   - **No internet connection** — Check your connection
   - **Voice not available** — Try refreshing voices or changing voice/language
   - **Invalid document** — Ensure the document is readable and not corrupted
   - **Disk space** — Bundles can be large; ensure sufficient disk space

### Bundle File Format

Bundles are ZIP archives with the following structure:

```
bundle.edgevoice.zip
├── manifest.json       # Metadata and sentence list
├── timings.json        # Audio timing events
├── document.txt        # Original text
└── audio/              # Directory with MP3 files
    ├── 000000.mp3      # First sentence
    ├── 000001.mp3      # Second sentence
    └── ...
```

You can inspect or extract bundles with any ZIP tool.

## Keyboard Shortcuts

Currently, keyboard shortcuts are not implemented. All features are available through the menu or toolbar buttons.

## Settings & Preferences

### Voice & Language

Saved automatically when changed:
- Selected language/locale
- Selected voice
- TTS playback rate

### Volume

Adjusted with the volume slider. Volume preference is saved between sessions.

### Storage

All preferences are stored in the system's application data directory:
- **Linux/Mac:** `~/.config/Monotoba/EdgeReader`
- **Windows:** `%APPDATA%\Monotoba\EdgeReader`

### Resetting Preferences

Delete the settings file to reset all preferences to defaults:
- **Linux:** `rm -rf ~/.config/Monotoba`
- **macOS:** `rm -rf ~/Library/Preferences/com.monotoba.edgereader.plist`
- **Windows:** Delete `HKEY_CURRENT_USER\Software\Monotoba\EdgeReader`

## Advanced Features

### Sentence Detection

Edge Reader automatically splits documents into sentences for synchronized playback. The algorithm:
- Respects common abbreviations (Mr., Dr., etc.)
- Handles quoted sentences
- Falls back to paragraph/line breaks for difficult text
- Chunks very long sentences (>900 characters) on punctuation or line breaks

### Temporary File Cleanup

**Offline bundles:**
Temporary bundle files are stored in:
- **Linux:** `/tmp/edge_reader_bundle_*`
- **macOS:** `/var/folders/.../edge_reader_bundle_*`
- **Windows:** `%TEMP%\edge_reader_bundle_*`

Automatically cleaned up when bundles are closed or the application exits.

**Live mode audio:**
Temporary live audio files are stored in:
- **Linux:** `/tmp/edge_reader_live_*`
- **macOS:** `/var/folders/.../edge_reader_live_*`
- **Windows:** `%TEMP%\edge_reader_live_*`

Automatically cleaned up when playback stops or the application exits.

In rare cases of interrupted shutdown, you may need to manually delete these directories.

### Future Enhancements

Planned features include:
- Word-level highlighting during playback
- Subtitle generation from timing data
- Batch bundle generation
- Integration with media players
