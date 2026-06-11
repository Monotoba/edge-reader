# Publishing Edge Reader to PyPI

This guide explains how to build and publish Edge Reader to PyPI.

## Prerequisites

1. **Python 3.10+** installed
2. **PyPI Account** - Create one at https://pypi.org/account/register/
3. **PyPI Token** - Generate at https://pypi.org/manage/account/tokens/

## Quick Start (Linux/macOS)

```bash
# 1. Update version
./scripts/version.sh

# 2. Build distribution
./scripts/build.sh

# 3. Publish to PyPI
export PYPI_TOKEN="your-token-here"
./scripts/publish.sh
```

## Quick Start (Windows)

```cmd
REM 1. Update version
python scripts/version.py

REM 2. Build distribution
scripts\build.bat

REM 3. Publish to PyPI
set PYPI_TOKEN=your-token-here
scripts\publish.bat
```

## Detailed Steps

### Step 1: Prepare Your Changes

Make sure all code is committed and pushed:

```bash
git status
git push origin main
```

### Step 2: Update Version

Use semantic versioning (MAJOR.MINOR.PATCH):

**Linux/macOS:**
```bash
./scripts/version.sh
```

**Windows:**
```bash
python scripts/version.py
```

Choose from:
- **Patch** (0.1.0 → 0.1.1): Bug fixes
- **Minor** (0.1.0 → 0.2.0): New features
- **Major** (0.1.0 → 1.0.0): Breaking changes

This script will:
- Update `pyproject.toml`
- Create a git commit
- Create a git tag

### Step 3: Build Distribution

**Linux/macOS:**
```bash
./scripts/build.sh
```

**Windows:**
```bash
scripts\build.bat
```

This creates:
- `.tar.gz` source distribution
- `.whl` wheel distribution

Files are saved in `dist/` directory.

### Step 4: Test the Build (Optional)

```bash
# Create a test virtual environment
python -m venv test_env
source test_env/bin/activate  # Linux/macOS
# or
test_env\Scripts\activate  # Windows

# Install from local wheel
pip install dist/edge_readaloud_pyside6-*.whl

# Test the command
edge-reader --help

# Cleanup
deactivate
rm -rf test_env
```

### Step 5: Publish to PyPI

Get your PyPI token from https://pypi.org/manage/account/tokens/

**Linux/macOS:**
```bash
export PYPI_TOKEN="pypi-your-token-here"
./scripts/publish.sh
```

**Windows:**
```bash
set PYPI_TOKEN=pypi-your-token-here
scripts\publish.bat
```

Or enter the token when prompted.

### Step 6: Push Git Tags

```bash
git push origin main
git push origin v0.1.0  # Replace with your version
```

## Verification

After publishing, verify on PyPI:

```bash
# Check package on PyPI
pip search edge-readaloud-pyside6  # or visit https://pypi.org/project/edge-readaloud-pyside6/

# Install from PyPI
pip install edge-readaloud-pyside6

# Run the installed package
edge-reader
```

## Troubleshooting

### "twine not found"
```bash
pip install twine
```

### "PYPI_TOKEN not set"
Set environment variable or enter token when prompted:
```bash
export PYPI_TOKEN="your-token"  # Linux/macOS
set PYPI_TOKEN=your-token        # Windows
```

### Build fails
```bash
# Clean and retry
rm -rf build/ dist/ src/*.egg-info/
./scripts/build.sh
```

### Upload fails
- Check token is valid at https://pypi.org/manage/account/tokens/
- Ensure version in `pyproject.toml` hasn't been published before
- Use `twine check dist/*` to validate

## PyPI Release Checklist

- [ ] All code committed and pushed
- [ ] Tests passing (`pytest`)
- [ ] Version updated
- [ ] `pyproject.toml` verified
- [ ] Distribution built
- [ ] Local test of wheel (optional)
- [ ] Published to PyPI
- [ ] Git tags pushed
- [ ] Verified on PyPI.org

## Release Notes

After publishing, create a GitHub release:

1. Go to https://github.com/Monotoba/edge-reader/releases
2. Click "Create a new release"
3. Select the tag you just pushed
4. Add release notes describing changes
5. Publish release

## Files Changed During Publishing

- `pyproject.toml` - Version number updated
- Git tags created (v0.1.0, v0.2.0, etc.)
- `dist/` directory - Contains distribution files

## Cleaning Up Old Builds

```bash
rm -rf build/ dist/ src/*.egg-info/
```

## More Information

- PyPI: https://pypi.org/
- Python Packaging Guide: https://packaging.python.org/
- Twine Documentation: https://twine.readthedocs.io/
