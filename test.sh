#!/bin/bash
# Test script for Edge Reader on Linux/macOS

set -e

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
else
    echo "WARNING: Virtual environment not found at .venv"
    echo "Run 'bash setup.sh' to set up the project first."
    exit 1
fi

# Check if pytest is available
if ! python -c "import pytest" 2>/dev/null; then
    echo "ERROR: pytest is not installed."
    echo "Run 'bash setup.sh' to install it."
    exit 1
fi

echo "Running tests..."
echo ""

# Run pytest with all provided arguments
pytest "$@"

TEST_RESULT=$?

echo ""
if [ $TEST_RESULT -eq 0 ]; then
    echo "✓ All tests passed!"
else
    echo "✗ Some tests failed (exit code: $TEST_RESULT)"
fi

exit $TEST_RESULT
