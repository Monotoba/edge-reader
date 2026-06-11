#!/bin/bash
# Publish script for uploading to PyPI

set -e

echo "📦 Publishing Edge Reader to PyPI..."
echo ""

# Check if distributions exist
if [ ! -d "dist/" ] || [ -z "$(ls -A dist/)" ]; then
    echo "❌ No distribution files found. Run ./scripts/build.sh first"
    exit 1
fi

# Ask for confirmation
echo "This will upload the following files to PyPI:"
ls -lh dist/
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 1
fi

# Check for PyPI token
if [ -z "$PYPI_TOKEN" ]; then
    echo "⚠️  PYPI_TOKEN environment variable not set."
    echo "Set it with: export PYPI_TOKEN='your-token-here'"
    read -p "Enter PyPI token (or Ctrl+C to cancel): " token
    PYPI_TOKEN="$token"
fi

# Upload to PyPI
echo ""
echo "Uploading to PyPI..."
python -m twine upload \
    --username "__token__" \
    --password "$PYPI_TOKEN" \
    dist/*

echo ""
echo "✅ Published successfully!"
echo ""
echo "View on PyPI: https://pypi.org/project/edge-readaloud-pyside6/"
