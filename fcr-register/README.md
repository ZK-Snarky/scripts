# Free Caller Registry - Semi-Automated Submission

Automates the FCR form at freecallerregistry.com. Pauses for manual email verification code entry.

## Setup

    pip install playwright
    playwright install chromium

Or run the setup script:

    bash fcr-setup.sh

## Usage

1. Edit the CONFIG section at the top of `fcr_register.py` with your business info and phone numbers
2. Run: `python fcr_register.py`
3. Script opens browser, fills everything, pauses for email code
4. Check your email, paste the code in the terminal
5. Script finishes the rest, pauses at review page for final check
