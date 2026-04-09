#!/bin/bash
# Quick setup for FCR Register script
# Run: bash fcr-setup.sh

PIP=$(command -v pip3 || command -v pip)
PYTHON=$(command -v python3 || command -v python)

if [ -z "$PIP" ]; then
    echo "Error: pip not found. Install Python 3 first:"
    echo "  brew install python"
    exit 1
fi

echo "Installing dependencies..."

# Try normal install first, fall back to trusted-host for corporate firewalls
$PIP install playwright 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Normal install failed (likely SSL/firewall). Retrying with trusted hosts..."
    $PIP install --trusted-host pypi.org --trusted-host files.pythonhosted.org playwright
fi

$PYTHON -m playwright install chromium

echo ""
echo "Done. Now edit fcr_register.py and fill in your info in the CONFIG section."
echo "Then run: $PYTHON fcr_register.py"
