import os
import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage

# ── CONFIG FROM ENVIRON ────────────────────────────────────────────────────────
EMAIL_ADDRESS = "tacofukuro@gmail.com"
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_NOTIFICATION = os.environ.get('EMAIL_NOTIFICATION')

# Debug: print env var status (never print passwords directly)
print(f"[DEBUG] EMAIL_ADDRESS = {EMAIL_ADDRESS!r}")
print(f"[DEBUG] EMAIL_PASSWORD set? {'yes' if EMAIL_PASSWORD else 'no'}")
print(f"[DEBUG] RAW TARGET_URL = {os.environ.get('TARGET_URL')!r}")
print(f"[DEBUG] RAW EMAIL_NOTIFICATION = {EMAIL_NOTIFICATION!r}")
print(f"[DEBUG] RAW SMTP_SERVER  = {os.environ.get('SMTP_SERVER')!r}")
print(f"[DEBUG] RAW SMTP_PORT    = {os.environ.get('SMTP_PORT')!r}\n")

# Use defaults if any of the above are missing/empty
_raw_url = os.environ.get("TARGET_URL", "").strip()
TARGET_URL = _raw_url or "https://dvivnv.carrd.co/#english"
print(f"[DEBUG] USING TARGET_URL = {TARGET_URL!r}")

SMTP_SERVER = os.environ.get("SMTP_SERVER", "").strip() or "smtp.gmail.com"

_port_str = os.environ.get("SMTP_PORT", "").strip()
SMTP_PORT = int(_port_str) if _port_str.isdigit() else 465
print(f"[DEBUG] USING SMTP = {SMTP_SERVER}:{SMTP_PORT}\n")
# ───────────────────────────────────────────────────────────────────────────────

def check_site() -> bool:
    print(f"[DEBUG] Checking site: {TARGET_URL}")
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(TARGET_URL, headers=headers)
    print(f"[DEBUG] HTTP status code: {resp.status_code}")
    resp.raise_for_status()

    # Define the list of target status strings
    target_keywords = [
        "<strong>open</strong>",
        "<strong>opened</strong>",
        "<strong>opening</strong>",
        "<strong>Open</strong>",
        "<strong>Opened</strong>",
        "<strong>Opening</strong>"
    ]

    # Check if any of the target keywords are present in the response text
    found = any(keyword in resp.text for keyword in target_keywords)
    print(f"[DEBUG] Found 'Commissions Open'?: {found}\n")
    return found

def send_email():
    print("[DEBUG] Sending email alert...")
    msg = EmailMessage()
    msg["Subject"] = "Commission Alert 🚨"
    msg["From"]    = EMAIL_ADDRESS
    msg["To"]      = EMAIL_NOTIFICATION
    msg.set_content(f"Duwi Check the commision page for the overlay: {TARGET_URL}")

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
    print("[DEBUG] Email sent successfully!\n")

def main():
    try:
        if check_site():
            send_email()
        else:
            print("[DEBUG] No change detected. No email sent.\n")
    except Exception as e:
        print(f"[ERROR] {e}")


if __name__ == "__main__":
    main()
