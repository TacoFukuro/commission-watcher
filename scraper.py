import os
import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage

# ── CONFIG FROM ENVIRON ────────────────────────────────────────────────────────
# In GitHub Actions, set these under Settings → Secrets and Variables → Actions
EMAIL_ADDRESS = os.environ["EMAIL_ADDRESS"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
TARGET_URL     = os.environ.get("TARGET_URL", "https://dvivnv.carrd.co/#english")
SMTP_SERVER    = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT      = int(os.environ.get("SMTP_PORT", 465))
# ───────────────────────────────────────────────────────────────────────────────

def check_site() -> bool:
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(TARGET_URL, headers=headers)
    resp.raise_for_status()
    return "commissions: closed" in resp.text

def send_email():
    msg = EmailMessage()
    msg["Subject"] = "Commission Alert 🚨"
    msg["From"]    = EMAIL_ADDRESS
    msg["To"]      = EMAIL_ADDRESS
    msg.set_content(f"Commissions are OPEN! Check here: {TARGET_URL}")

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

def main():
    try:
        if check_site():
            send_email()
    except Exception as e:
        # This will surface errors in your GitHub Actions or Render logs
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    main()
