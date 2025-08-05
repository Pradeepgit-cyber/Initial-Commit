import smtplib
import pandas as pd
from email.message import EmailMessage
import os
import mimetypes

# CSV path
csv_path ='/Users/pradeepbaraik/PycharmProjects/PythonProject3/Emails.csv'
data = pd.read_csv(csv_path)

# Gmail credentials
EMAIL_ADDRESS = 'pradeep.kr.baraik@gmail.com'
EMAIL_PASSWORD = 'gfdb cebi bztm aded'  # App Password

# Attachment file (resume)
attachment_path = '/Users/pradeepbaraik/PycharmProjects/PythonProject3/Revised Latest Resume-Pradeep-2025 (1).pdf'
if not os.path.isfile(attachment_path):
    raise FileNotFoundError(f"Attachment not found: {attachment_path}")

# Email body (same for all)
email_body = """\
Dear Hiring Manager,

I am writing to apply for the Senior QA Engineer position. With over 5+ years of experience in quality assurance and software testing, I bring a solid background in both manual and automated testing practices.

My expertise includes tools such as Manual Testing, Postman, JIRA, Jmeter, Locust, Python(Basics), Selenium and experience in test planning, execution, and defect management across agile environments. I have consistently contributed to improving product quality and release efficiency in previous roles.

Please find my resume attached for your consideration. I am available for further discussion at your convenience.

Thank you for your time and consideration.

Sincerely,  
Pradeep Kumar Baraik  
7053355200
"""

# Setup SMTP server
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

# Loop through recipients and send emails
for index, row in data.iterrows():
    msg = EmailMessage()
    msg['Subject'] = 'Application for Senior QA Engineer Role(Manual)'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = row['Email']
    msg.set_content(email_body)

    # Add attachment
    mime_type, _ = mimetypes.guess_type(attachment_path)
    mime_type = mime_type or 'application/octet-stream'
    maintype, subtype = mime_type.split('/')

    with open(attachment_path, 'rb') as f:
        msg.add_attachment(f.read(), maintype=maintype, subtype=subtype, filename=os.path.basename(attachment_path))

    try:
        server.send_message(msg)
        print(f"✅ Email sent to {row['Email']}")
    except Exception as e:
        print(f"❌ Failed to send email to {row['Email']}: {e}")

server.quit()


