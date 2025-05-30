import os
import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()  # pull EMAIL_ADDRESS, EMAIL_PASSWORD from .env

# You can also move URL into .env if you like
URL = os.getenv("TARGET_URL", "https://dvivnv.carrd.co/#english")

def check_site():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    return "commissions: closed" in soup.text  # adjust your match text

def send_email():
    msg = EmailMessage()
    msg.set_content(f"🚨 Commissions are Close! Visit: {URL}")
    msg["Subject"] = "Commission Alert"
    msg["From"] = os.getenv("EMAIL_ADDRESS")
    msg["To"]   = os.getenv("EMAIL_NOTIFICATION=")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_PASSWORD"))
        smtp.send_message(msg)

def main():
    try:
        if check_site():
            send_email()
    except Exception as e:
        # In Render you can view logs for these exceptions
        print(f"Error during scraper run: {e}")

if __name__ == "__main__":
    main()
