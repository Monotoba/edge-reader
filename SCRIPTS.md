# Edge Reader — Scripts Documentation

This document describes all setup, run, and test scripts included with Edge Reader.

## Overview

| Script | Platform | Type | Purpose |
|--------|----------|------|---------|
| `setup.sh` | Linux/macOS | Bash | Create venv and install dependencies |
| `setup.bat` | Windows | Batch | Create venv and install dependencies |
| `setup.ps1` | Windows | PowerShell | Create venv and install dependencies |
| `run.sh` | Linux/macOS | Bash | Run the Edge Reader GUI |
| `run.bat` | Windows | Batch | Run the Edge Reader GUI |
| `run.ps1` | Windows | PowerShell | Run the Edge Reader GUI |
| `test.sh` | Linux/macOS | Bash | Run pytest test suite |
| `test.bat` | Windows | Batch | Run pytest test suite |
| `test.ps1` | Windows | PowerShell | Run pytest test suite |

## Setup Scripts

### `setup.sh` (Linux/macOS)

Creates a Python virtual environment and installs Edge Reader with dependencies.

**Usage:**
```bash
bash setup.sh
```

**What it does:**
1. Checks Python version (requires 3.10+)
2. Creates `.venv/` directory (or reuses existing)
3. Activates the virtual environment
4. Upgrades pip
5. Installs Edge Reader in editable mode with `[dev]` extras (includes pytest, ruff)
6. Verifies installation

**Options:**
- None (interactive prompts if venv exists)

**Environment:**
- Works with `bash` or `sh`
- Requires Python 3.10+ in PATH
- Creates `.venv` directory in the project root

---

### `setup.bat` (Windows Command Prompt)

Creates a Python virtual environment and installs Edge Reader with dependencies.

**Usage:**
```cmd
setup.bat
```

**What it does:**
1. Checks Python version (requires 3.10+)
2. Creates `.venv\` directory (or reuses existing)
3. Activates the virtual environment
4. Upgrades pip
5. Installs Edge Reader in editable mode with `[dev]` extras (includes pytest, ruff)
6. Verifies installation

**Options:**
- None (interactive prompts if venv exists)

**Environment:**
- Requires Windows Command Prompt or PowerShell
- Requires Python 3.10+ in PATH
- Creates `.venv` directory in the project root

---

### `setup.ps1` (Windows PowerShell)

Creates a Python virtual environment and installs Edge Reader with dependencies.

**Usage:**
```powershell
.\setup.ps1
```

**What it does:**
1. Checks Python version (requires 3.10+)
2. Creates `.venv\` directory (or reuses existing)
3. Activates the virtual environment
4. Upgrades pip
5. Installs Edge Reader in editable mode with `[dev]` extras (includes pytest, ruff)
6. Verifies installation

**Options:**
- `-Force` — Force creation of new venv, deleting existing one

**Examples:**
```powershell
# Normal setup
.\setup.ps1

# Force fresh setup
.\setup.ps1 -Force
```

**Environment:**
- Requires Windows PowerShell 5.0+
- Requires Python 3.10+ in PATH
- Creates `.venv` directory in the project root
- May require execution policy change: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

---

## Run Scripts

### `run.sh` (Linux/macOS)

Activates the virtual environment and runs the Edge Reader GUI application.

**Usage:**
```bash
bash run.sh [OPTIONS]
```

**What it does:**
1. Checks if `.venv/` exists
2. Activates the virtual environment
3. Verifies Edge Reader is installed
4. Launches `python -m edge_reader`

**Options:**
- Any options passed are forwarded to the Edge Reader application
- See `python -m edge_reader --help` for application options

**Examples:**
```bash
bash run.sh                 # Run normally
bash run.sh --help          # Show help
```

**Environment:**
- Requires `.venv/` directory (created by `setup.sh`)
- Requires Edge Reader to be installed in venv

---

### `run.bat` (Windows Command Prompt)

Activates the virtual environment and runs the Edge Reader GUI application.

**Usage:**
```cmd
run.bat [OPTIONS]
```

**What it does:**
1. Checks if `.venv\` exists
2. Activates the virtual environment
3. Verifies Edge Reader is installed
4. Launches `python -m edge_reader`

**Options:**
- Any options passed are forwarded to the Edge Reader application
- See `python -m edge_reader --help` for application options

**Examples:**
```cmd
run.bat                     REM Run normally
run.bat --help              REM Show help
```

**Environment:**
- Requires `.venv\` directory (created by `setup.bat`)
- Requires Edge Reader to be installed in venv

---

### `run.ps1` (Windows PowerShell)

Activates the virtual environment and runs the Edge Reader GUI application.

**Usage:**
```powershell
.\run.ps1 [OPTIONS]
```

**What it does:**
1. Checks if `.venv\` exists
2. Activates the virtual environment
3. Verifies Edge Reader is installed
4. Launches `python -m edge_reader`

**Options:**
- Any options passed are forwarded to the Edge Reader application
- See `python -m edge_reader --help` for application options

**Examples:**
```powershell
.\run.ps1                   # Run normally
.\run.ps1 --help            # Show help
```

**Environment:**
- Requires `.venv\` directory (created by `setup.ps1`)
- Requires Edge Reader to be installed in venv
- Requires execution policy: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

---

## Test Scripts

### `test.sh` (Linux/macOS)

Runs the Edge Reader test suite using pytest.

**Usage:**
```bash
bash test.sh [PYTEST_OPTIONS]
```

**What it does:**
1. Checks if `.venv/` exists
2. Activates the virtual environment
3. Verifies pytest is installed
4. Runs `pytest` with provided options

**Options:**
- Any pytest options can be passed through
- Common: `-v` (verbose), `-x` (stop on first failure), `tests/test_bundle.py` (specific file)

**Examples:**
```bash
bash test.sh                            # Run all tests
bash test.sh -v                         # Verbose output
bash test.sh -x                         # Stop on first failure
bash test.sh tests/test_bundle.py      # Test single file
bash test.sh -k "test_document"        # Run specific test by name
```

**Environment:**
- Requires `.venv/` directory (created by `setup.sh`)
- Requires pytest to be installed (included in `[dev]` extras)

---

### `test.bat` (Windows Command Prompt)

Runs the Edge Reader test suite using pytest.

**Usage:**
```cmd
test.bat [PYTEST_OPTIONS]
```

**What it does:**
1. Checks if `.venv\` exists
2. Activates the virtual environment
3. Verifies pytest is installed
4. Runs `pytest` with provided options

**Options:**
- Any pytest options can be passed through
- Common: `-v` (verbose), `-x` (stop on first failure), `tests/test_bundle.py` (specific file)

**Examples:**
```cmd
test.bat                            REM Run all tests
test.bat -v                         REM Verbose output
test.bat -x                         REM Stop on first failure
test.bat tests/test_bundle.py      REM Test single file
test.bat -k "test_document"        REM Run specific test by name
```

**Environment:**
- Requires `.venv\` directory (created by `setup.bat`)
- Requires pytest to be installed (included in `[dev]` extras)

---

### `test.ps1` (Windows PowerShell)

Runs the Edge Reader test suite using pytest.

**Usage:**
```powershell
.\test.ps1 [PYTEST_OPTIONS]
```

**What it does:**
1. Checks if `.venv\` exists
2. Activates the virtual environment
3. Verifies pytest is installed
4. Runs `pytest` with provided options

**Options:**
- Any pytest options can be passed through
- Common: `-v` (verbose), `-x` (stop on first failure), `tests/test_bundle.py` (specific file)

**Examples:**
```powershell
.\test.ps1                            # Run all tests
.\test.ps1 -v                         # Verbose output
.\test.ps1 -x                         # Stop on first failure
.\test.ps1 tests/test_bundle.py      # Test single file
.\test.ps1 -k "test_document"        # Run specific test by name
```

**Environment:**
- Requires `.venv\` directory (created by `setup.ps1`)
- Requires pytest to be installed (included in `[dev]` extras)
- Requires execution policy: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

---

## Troubleshooting Scripts

### "Permission denied" on Linux/macOS

Make scripts executable:
```bash
chmod +x setup.sh run.sh test.sh
```

### "Cannot be loaded because running scripts is disabled" on Windows PowerShell

Allow script execution:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### "Module not found" errors

Run setup script again:
```bash
bash setup.sh          # Linux/macOS
setup.bat              # Windows (cmd)
.\setup.ps1            # Windows (PowerShell)
```

### Virtual environment won't activate

Try removing and recreating:
```bash
rm -rf .venv           # Linux/macOS
rmdir /s /q .venv      # Windows
bash setup.sh          # Then run setup again
```

---

## Advanced Usage

### Development Workflow

```bash
# Setup
bash setup.sh

# Activate venv once
source .venv/bin/activate

# Then during development:
python -m edge_reader        # Run app directly
pytest -v                    # Run tests
ruff check src/ tests/       # Check code style
ruff format src/ tests/      # Format code
```

### Running Specific Tests

```bash
bash test.sh -v tests/test_bundle.py       # Specific test file
bash test.sh -k "test_extract"             # Tests matching pattern
bash test.sh --lf                          # Last failed tests
bash test.sh --ff                          # Failed first, then others
```

### Continuous Testing

Watch for changes and rerun tests:
```bash
# Install pytest-watch
pip install pytest-watch

# Watch and rerun
ptw

# With options
ptw -- -v tests/
```

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Failure (setup error, test failure, missing module, etc.) |

---

## Environment Variables

Scripts respect standard environment variables:

- `PYTHONPATH` — Python module search path
- `PATH` — Executable search path (for Python, ebook-convert, etc.)
- `PYTHONUNBUFFERED` — Unbuffered Python output (optional)

---

## See Also

- `QUICKSTART.md` — Quick start guide
- `SETUP.md` — Detailed setup documentation
- `README.md` — Feature overview
- `help/USER_MANUAL.md` — User guide
- `help/TROUBLESHOOTING.md` — Troubleshooting tips
