from tools.vendor_finder import get_mock_vendors
from tools.email_writer import generate_quote_email
from tools.email_sender import send_email
from tools.form_writer import generate_form_submission
from tools.report_generator import generate_report
import os
from dotenv import load_dotenv

load_dotenv()

SERVICE = "window replacement"
CITY = "Seattle"
DETAILS = "We have two cracked windows in a single-family home." # Replace with more complex details 
USER_NAME = "Jeffrey Brown"
USER_EMAIL = "jeff@example.com" # Replace with your email

vendors = get_mock_vendors(SERVICE, CITY)
responses = {}

for v in vendors:
    if "email" in v:
        body = generate_quote_email(SERVICE, CITY, DETAILS)
        try:
            send_email(
                to_email=v["email"],
                subject=f"Quote request: {SERVICE} in {CITY}",
                body=body,
                from_email=USER_EMAIL,
                smtp_user=os.getenv("SMTP_USER"),
                smtp_pass=os.getenv("SMTP_PASS")
            )
            responses[v["name"]] = "Email sent (waiting for reply)"
        except Exception as e:
            responses[v["name"]] = f"Failed to send: {e}"
    elif "contact_form_url" in v:
        form_fill = generate_form_submission(SERVICE, CITY, DETAILS, USER_NAME, USER_EMAIL)
        responses[v["name"]] = f"Form URL: {v['contact_form_url']}\n\nSuggested Input:\n{form_fill}"
    else:
        responses[v["name"]] = "No contact method available."

generate_report(vendors, responses)
print("✅ Done. Report saved to report.md")
