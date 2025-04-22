import smtplib
from email.message import EmailMessage
import os

USE_MOCK_EMAIL = os.getenv("USE_MOCK_EMAIL", "true").lower() == "true"

def send_email(to_email: str, subject: str, body: str, from_email: str, smtp_user: str, smtp_pass: str):
    if USE_MOCK_EMAIL:
        print(f"[MOCK EMAIL] To: {to_email}\nSubject: {subject}\n---\n{body}\n---\n")

    else:
      msg = EmailMessage()
      msg.set_content(body)
      msg['Subject'] = subject
      msg['From'] = from_email
      msg['To'] = to_email

      with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
          smtp.login(smtp_user, smtp_pass)
          # smtp.send_message(msg)
