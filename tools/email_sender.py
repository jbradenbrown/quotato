import smtplib
from email.message import EmailMessage

def send_email(to_email: str, subject: str, body: str, from_email: str, smtp_user: str, smtp_pass: str):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(smtp_user, smtp_pass)
        smtp.send_message(msg)
