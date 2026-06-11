#!/bin/bash
# Build script for creating distribution packages

set -e

echo "🔨 Building Edge Reader package..."

# Clean old builds
echo "Cleaning previous builds..."
rm -rf build/ dist/ src/*.egg-info/

# Install build tools if needed
echo "Ensuring build tools are installed..."
python -m pip install --upgrade build twine

# Build distribution
echo "Building distribution..."
python -m build

echo ""
echo "✅ Build complete!"
echo "Distribution files created in dist/"
echo ""
echo "Files ready:"
ls -lh dist/
