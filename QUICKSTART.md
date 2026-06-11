# Edge Reader — Quick Start Guide

Get Edge Reader up and running in 2 minutes.

## Choose Your Platform

### Linux / macOS

```bash
# 1. Setup (one time)
bash setup.sh

# 2. Run the app
bash run.sh

# 3. Run tests
bash test.sh
```

### Windows (PowerShell) — Recommended

```powershell
# 1. Setup (one time)
.\setup.ps1

# 2. Run the app
.\run.ps1

# 3. Run tests
.\test.ps1
```

### Windows (Command Prompt)

```cmd
REM 1. Setup (one time)
setup.bat

REM 2. Run the app
run.bat

REM 3. Run tests
test.bat
```

---

## What These Scripts Do

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `setup.sh` / `setup.bat` / `setup.ps1` | Creates Python virtual environment and installs dependencies | First time only (or when dependencies change) |
| `run.sh` / `run.bat` / `run.ps1` | Starts the Edge Reader GUI application | Every time you want to use the app |
| `test.sh` / `test.bat` / `test.ps1` | Runs the unit test suite | When verifying installation or after code changes |

---

## Manual Setup (If Scripts Don't Work)

If the scripts encounter issues, you can set up manually:

### 1. Create and activate a virtual environment

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

### 2. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

### 3. Run the app or tests

```bash
python -m edge_reader    # Run the app
pytest                    # Run tests
```

---

## Common Issues

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module named edge_reader` | Run `bash setup.sh` (or equivalent for your OS) |
| Permission denied on `setup.sh` | Run `chmod +x setup.sh` |
| PowerShell execution policy error | Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| Audio playback fails on Linux | See SETUP.md → Linux → Audio Playback Setup |
| PySide6 fails to start on Linux | See SETUP.md → Linux → Display Server Setup |

---

## Next Steps

1. **Read the Manual:** See `help/USER_MANUAL.md`
2. **Learn the Details:** See `SETUP.md` for platform-specific configuration
3. **Report Issues:** Check `help/TROUBLESHOOTING.md`

---

## Features at a Glance

- Load text, documents, PDFs, EPUB ebooks
- **Play immediately:** Listen with live audio synthesis (internet required)
- **Or generate offline:** Create bundles (`.edgevoice.zip`) for replay without internet
- Sentence-by-sentence highlighting during playback
- Support for multiple languages and voices
- TTS speed control
- Cross-platform (Linux, macOS, Windows)

---

Need help? See SETUP.md or help/TROUBLESHOOTING.md
