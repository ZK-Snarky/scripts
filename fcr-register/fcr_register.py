#!/usr/bin/env python3
"""
Free Caller Registry — Semi-Automated Submission
=================================================
Automates the FCR form at freecallerregistry.com.
Pauses for manual email verification code entry.

Setup:
  1. Install Python 3.9+ if not already installed
  2. pip install playwright
  3. playwright install chromium
  4. Edit the CONFIG section below with your info
  5. python fcr_register.py

Usage:
  - Script opens the browser and fills everything
  - When it needs the email code, it pauses and asks you
  - You check your email, paste the code in the terminal
  - Script finishes the rest
"""

# ============================================================
# CONFIG — Edit this section
# ============================================================

EMAIL = "seb@example.com"  # Business email (verification code sent here)

BUSINESS = {
    "name": "Your Business Name",
    "street": "123 Main St",
    "city": "Scottsdale",
    "state": "Arizona",       # Must match dropdown text exactly
    "zip": "85251",
    "website": "https://yoursite.com",
    "contact_name": "Seb Taillieu",
    "contact_phone": "4805551234",  # 10 digits, no dashes
    "call_purpose": "Financial Services",  # Dropdown value
    "calls_per_month": "1 - 100",          # Dropdown value
}

PHONE_NUMBERS = [
    "4805551234",
    "6025551234",
    # Add more numbers here (up to 20)
]

HEADLESS = False  # Set True to hide browser (not recommended for semi-auto)

# ============================================================
# END CONFIG
# ============================================================

import sys
import time


def check_deps():
    try:
        import playwright
    except ImportError:
        print("Missing dependency. Run:")
        print("  pip install playwright")
        print("  playwright install chromium")
        sys.exit(1)


def run():
    from playwright.sync_api import sync_playwright

    print("=" * 50)
    print("  Free Caller Registry - Semi-Auto")
    print("=" * 50)
    print()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        page = context.new_page()

        # Step 1: Open FCR
        print("[1/6] Loading Free Caller Registry...")
        page.goto("https://www.freecallerregistry.com/fcr/", wait_until="networkidle")
        page.wait_for_timeout(2000)

        # Step 2: Enter email and send verification code
        print(f"[2/6] Sending verification code to {EMAIL}...")
        email_input = page.locator('input[type="email"], input[name="email"], input[placeholder*="email" i]')
        if email_input.count() == 0:
            email_input = page.locator('input').first
        email_input.fill(EMAIL)

        # Click send verification code button
        send_btn = page.locator('text=send verification code')
        if send_btn.count() == 0:
            send_btn = page.locator('button:has-text("send"), a:has-text("send")')
        send_btn.first.click()
        page.wait_for_timeout(3000)

        # Step 3: Wait for user to enter verification code
        print()
        print("  >>> CHECK YOUR EMAIL <<<")
        print("  Enter the verification code below.")
        print()
        code = input("  Verification code: ").strip()

        if not code:
            print("  No code entered. Exiting.")
            browser.close()
            sys.exit(1)

        print()
        print("[3/6] Entering verification code...")

        # Find and fill the verification code input
        code_inputs = page.locator('input[maxlength="6"], input[maxlength="5"], input[maxlength="4"]')
        if code_inputs.count() > 0:
            code_inputs.first.fill(code)
        else:
            # Fallback: find any visible input that appeared after clicking send
            all_inputs = page.locator('input:visible')
            for i in range(all_inputs.count()):
                inp = all_inputs.nth(i)
                placeholder = (inp.get_attribute("placeholder") or "").lower()
                if "code" in placeholder or "verification" in placeholder:
                    inp.fill(code)
                    break
            else:
                if all_inputs.count() > 1:
                    all_inputs.nth(1).fill(code)

        # Click verify and continue
        verify_btn = page.locator('text=verify and continue')
        if verify_btn.count() == 0:
            verify_btn = page.locator('button:has-text("verify")')
        verify_btn.first.click()
        page.wait_for_timeout(3000)

        # Step 4: Fill business details
        print("[4/6] Filling business details...")

        def fill_field(label_text, value):
            """Find a field by its label or placeholder and fill it."""
            label = page.locator(f'label:has-text("{label_text}")')
            if label.count() > 0:
                for_attr = label.first.get_attribute("for")
                if for_attr:
                    page.locator(f'#{for_attr}').fill(value)
                    return
            field = page.locator(f'input[placeholder*="{label_text}" i]')
            if field.count() > 0:
                field.first.fill(value)
                return
            print(f"    [!] Could not auto-fill: {label_text}")

        fill_field("Business name", BUSINESS["name"])
        fill_field("street address", BUSINESS["street"])
        fill_field("City", BUSINESS["city"])
        fill_field("Zip", BUSINESS["zip"])
        fill_field("website", BUSINESS["website"])
        fill_field("contact name", BUSINESS["contact_name"])
        fill_field("contact phone", BUSINESS["contact_phone"])

        # Handle state dropdown
        state_select = page.locator('select').filter(
            has=page.locator(f'option:text-is("{BUSINESS["state"]}")')
        )
        if state_select.count() > 0:
            state_select.first.select_option(label=BUSINESS["state"])

        # Handle call purpose dropdown
        purpose_select = page.locator('select').filter(
            has=page.locator('option:text-is("Attorney / Law")')
        )
        if purpose_select.count() > 0:
            purpose_select.first.select_option(label=BUSINESS["call_purpose"])

        # Handle calls per month dropdown
        calls_select = page.locator('select').filter(
            has=page.locator('option:text-is("1 - 100")')
        )
        if calls_select.count() > 0:
            calls_select.first.select_option(label=BUSINESS["calls_per_month"])

        # Click continue to next step
        cont_btn = page.locator('text=continue to next step')
        if cont_btn.count() == 0:
            cont_btn = page.locator('button:has-text("continue")')
        if cont_btn.count() > 0:
            cont_btn.first.click()
            page.wait_for_timeout(2000)

        # Step 5: Add phone numbers
        print("[5/6] Adding phone numbers...")
        if not PHONE_NUMBERS:
            print("    [!] No phone numbers in config. Skipping.")
        else:
            # Look for the text input for individual number entry
            number_input = page.locator(
                'input[placeholder*="phone" i], input[placeholder*="number" i], textarea'
            )
            if number_input.count() > 0:
                field = number_input.first
                tag = field.evaluate("el => el.tagName.toLowerCase()")
                if tag == "textarea":
                    field.fill("\n".join(PHONE_NUMBERS))
                else:
                    for num in PHONE_NUMBERS:
                        field.fill(num)
                        add_btn = page.locator('button:has-text("add"), button:has-text("+")')
                        if add_btn.count() > 0:
                            add_btn.first.click()
                            page.wait_for_timeout(500)

            # Click continue to final step
            cont_btn = page.locator('text=continue to final step')
            if cont_btn.count() == 0:
                cont_btn = page.locator('button:has-text("continue")')
            if cont_btn.count() > 0:
                cont_btn.first.click()
                page.wait_for_timeout(2000)

        # Step 6: Review and submit
        print("[6/6] Review page reached.")
        print()
        print("  >>> REVIEW THE FORM IN THE BROWSER <<<")
        print("  The script has filled everything it can.")
        print("  Check the page, accept the terms checkbox,")
        print("  then click 'Submit Your Registration' manually.")
        print()
        print("  Press Enter here when done (or Ctrl+C to quit).")
        input()

    print()
    print("Done. Browser closed.")


if __name__ == "__main__":
    check_deps()
    run()
