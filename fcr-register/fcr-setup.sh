#!/bin/bash
# Quick setup for FCR Register script
# Run: bash fcr-setup.sh

# Use pip3 if pip not found
PIP=$(command -v pip3 || command -v pip)
PYTHON=$(command -v python3 || command -v python)

if [ -z "$PIP" ]; then
    echo "Error: pip not found. Install Python 3 first:"
    echo "  brew install python"
    exit 1
fi

echo "Installing dependencies..."
$PIP install playwright
$PYTHON -m playwright install chromium

echo ""
echo "Done. Now edit fcr_register.py and fill in your info in the CONFIG section."
echo "Then run: $PYTHON fcr_register.py"
