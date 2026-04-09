#!/bin/bash
# Quick setup for FCR Register script
# Run: bash fcr-setup.sh

echo "Installing dependencies..."
pip install playwright
playwright install chromium

echo ""
echo "Done. Now edit fcr_register.py and fill in your info in the CONFIG section."
echo "Then run: python fcr_register.py"
