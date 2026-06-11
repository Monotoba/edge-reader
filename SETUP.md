# Setup Guide for Edge Reader

Edge Reader is a cross-platform PySide6 desktop application that reads aloud documents and ebooks using Microsoft Edge's neural text-to-speech engine.

## System Requirements

- **Python**: 3.10 or newer
- **Memory**: 2GB RAM minimum
- **Disk Space**: 500MB (including dependencies)
- **Internet**: Required for initial setup and audio generation

## Operating System Requirements

### Linux
- GStreamer plugins for audio playback
- Qt/XCB support libraries
- X11 or Wayland display server

### macOS
- macOS 10.15 or newer
- Xcode Command Line Tools (for compilation of native dependencies)

### Windows
- Windows 10 or newer
- Visual C++ Build Tools (optional, for compiling native dependencies)

## Quick Start (All Platforms)

The easiest way to set up Edge Reader is to use the provided setup script for your platform:

**Linux/macOS:**
```bash
bash setup.sh
```

**Windows (PowerShell):**
```powershell
.\setup.ps1
```

**Windows (Command Prompt):**
```cmd
setup.bat
```

These scripts will:
1. Create a Python virtual environment
2. Upgrade pip
3. Install dependencies
4. Install the project in editable mode

---

## Manual Setup (All Platforms)

### Step 1: Create a Virtual Environment

**Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
python -m venv .venv
.venv\Scripts\activate
```

### Step 2: Upgrade pip

```bash
python -m pip install --upgrade pip
```

### Step 3: Install Dependencies

```bash
pip install -e ".[dev]"
```

The `[dev]` extra includes testing tools (pytest, ruff).

### Step 4: Verify Installation

```bash
python -m edge_reader --help
```

Or simply run the app:
```bash
python -m edge_reader
```

---

## Platform-Specific Configuration

### Linux

#### Audio Playback Setup

Edge Reader uses PySide6's QtMultimedia for audio playback, which relies on GStreamer plugins. If MP3 playback fails, install the multimedia plugins:

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install gstreamer1.0-plugins-base \
                 gstreamer1.0-plugins-good \
                 gstreamer1.0-plugins-bad \
                 gstreamer1.0-plugins-ugly
```

**Fedora/RHEL:**
```bash
sudo dnf install gstreamer1-plugins-base \
                 gstreamer1-plugins-good \
                 gstreamer1-plugins-bad-free \
                 gstreamer1-plugins-ugly-free
```

**Arch Linux:**
```bash
sudo pacman -S gst-plugins-base gst-plugins-good gst-plugins-bad gst-plugins-ugly
```

#### Display Server Setup

If PySide6 fails to start on minimal Linux installs, install XCB support packages:

**Ubuntu/Debian:**
```bash
sudo apt install libxcb-cursor0 libxcb-xinerama0
```

**Fedora/RHEL:**
```bash
sudo dnf install libxcb xcb-util-cursor
```

### macOS

No additional configuration is typically required. If you encounter compilation issues with native dependencies, install Xcode Command Line Tools:

```bash
xcode-select --install
```

### Windows

No additional configuration is required. If you need to compile native extensions, install:

- [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

Or install Visual Studio Community with the "Desktop development with C++" workload.

---

## Optional: Calibre Integration

To support MOBI/AZW/AZW3 and other ebook formats, install Calibre:

**Linux:**
```bash
# Ubuntu/Debian
sudo apt install calibre

# Fedora
sudo dnf install calibre

# Arch
sudo pacman -S calibre
```

**macOS:**
```bash
# Via Homebrew
brew install calibre

# Or download from https://calibre-ebook.com/download
```

**Windows:**
Download and install from [Calibre's official website](https://calibre-ebook.com/download).

Verify installation:
```bash
ebook-convert --version
```

---

## Running the Application

Once setup is complete, run the app using:

**All Platforms:**
```bash
python -m edge_reader
```

**Or if installed with entry point:**
```bash
edge-reader
```

**Quick run with script:**

- **Linux/macOS:** `bash run.sh`
- **Windows (PowerShell):** `.\run.ps1`
- **Windows (Command Prompt):** `run.bat`

---

## Running Tests

Verify your installation by running the test suite:

**All Platforms:**
```bash
pytest
```

**Or with script:**

- **Linux/macOS:** `bash test.sh`
- **Windows (PowerShell):** `.\test.ps1`
- **Windows (Command Prompt):** `test.bat`

---

## Troubleshooting

### "No module named edge_reader"

Ensure your virtual environment is activated and dependencies are installed:
```bash
# Activate venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Reinstall
pip install -e ".[dev]"
```

### Audio playback fails on Linux

Install GStreamer plugins (see [Audio Playback Setup](#audio-playback-setup) above).

### PySide6 fails to start on Linux

Install XCB support packages (see [Display Server Setup](#display-server-setup) above).

### "ebook-convert not found"

Install Calibre (see [Optional: Calibre Integration](#optional-calibre-integration) above).

### Permission denied on macOS/Linux

If you get "Permission denied" when running scripts, make them executable:
```bash
chmod +x setup.sh run.sh test.sh
```

### ModuleNotFoundError for dependencies

Ensure pip is upgraded and reinstall dependencies:
```bash
python -m pip install --upgrade pip
pip install --upgrade -e ".[dev]"
```

---

## Development Workflow

### Project Structure

```
.
├── src/edge_reader/          # Main package
│   ├── main.py              # PySide6 GUI and playback
│   ├── document.py          # File/document extraction
│   ├── textseg.py           # Sentence/chunk splitting
│   ├── tts_edge.py          # Edge-TTS synthesis
│   ├── bundle.py            # Bundle creation/loading
│   └── ...
├── tests/                    # Unit tests
├── SETUP.md                  # This file
├── setup.sh / setup.bat      # Setup scripts
├── run.sh / run.bat          # Run scripts
├── test.sh / test.bat        # Test scripts
└── pyproject.toml            # Project metadata
```

### Code Quality

Format and lint code with [Ruff](https://github.com/astral-sh/ruff):

```bash
# Check
ruff check src/ tests/

# Format
ruff format src/ tests/
```

### Testing

Run the test suite to verify changes:

```bash
pytest              # All tests
pytest -v           # Verbose
pytest tests/test_bundle.py  # Single file
```

---

## Getting Help

- **Documentation:** See `README.md` for features and usage
- **User Manual:** See `help/USER_MANUAL.md` for detailed instructions
- **Troubleshooting:** See `help/TROUBLESHOOTING.md` or this guide
- **Issues:** Report bugs or request features on GitHub

---

## License

MIT License — See LICENSE file for details.
