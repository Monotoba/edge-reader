#!/bin/bash
# Setup script for Edge Reader on Linux/macOS
# Creates virtual environment, installs dependencies, and sets up the project

set -e  # Exit on error

echo "=================================================="
echo "Edge Reader Setup for Linux/macOS"
echo "=================================================="
echo ""

# Check Python version
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed."
    echo "Please install Python 3.10 or newer from https://www.python.org/"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "Found Python $PYTHON_VERSION"

if ! python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)'; then
    echo "ERROR: Python 3.10 or newer is required."
    echo "Current version: $PYTHON_VERSION"
    exit 1
fi
echo "✓ Python version check passed"
echo ""

# Create virtual environment
if [ -d ".venv" ]; then
    echo "Virtual environment already exists at .venv"
    read -p "Do you want to remove it and create a new one? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Removing existing virtual environment..."
        rm -rf .venv
        echo "✓ Removed"
    fi
fi

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo "✓ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip --quiet
echo "✓ pip upgraded"
echo ""

# Install project in editable mode with dev dependencies
echo "Installing Edge Reader and dependencies..."
echo "This may take a few minutes..."
pip install -e ".[dev]"
echo "✓ Installation complete"
echo ""

# Verify installation
echo "Verifying installation..."
if python -c "import edge_reader" 2>/dev/null; then
    echo "✓ Edge Reader module found"
else
    echo "WARNING: Edge Reader module not found. Try running:"
    echo "  source .venv/bin/activate"
    echo "  pip install -e '.[dev]'"
fi
echo ""

echo "=================================================="
echo "Setup Complete!"
echo "=================================================="
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment:"
echo "   source .venv/bin/activate"
echo ""
echo "2. Run the application:"
echo "   python -m edge_reader"
echo "   or: edge-reader"
echo ""
echo "3. Run tests:"
echo "   pytest"
echo ""
echo "For platform-specific configuration, see SETUP.md"
echo ""
