#!/bin/bash
# Run script for Edge Reader on Linux/macOS

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
else
    echo "WARNING: Virtual environment not found at .venv"
    echo "Run 'bash setup.sh' to set up the project first."
    exit 1
fi

# Check if edge_reader module is available
if ! python -c "import edge_reader" 2>/dev/null; then
    echo "ERROR: Edge Reader is not installed."
    echo "Run 'bash setup.sh' to install it."
    exit 1
fi

echo "Starting Edge Reader..."
echo ""

# Run the application
python -m edge_reader "$@"
