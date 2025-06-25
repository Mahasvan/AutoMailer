from automailer import AutoMailer
from automailer import TemplateModel, TemplateEngine


class MySchema(TemplateModel):
    name: str
    committee: str
    allotment: str
    email: str

with open("body.txt", "r") as f:
    body = f.read()

with open("subject.txt", "r") as f:
    subject = f.read()

template = TemplateEngine(subject=subject, body_text=body)

recipients = [
    {"name": "John", "committee": "ECOSOC", "allotment": "Algeria", "email": "myEmail@gmail.com"},
    {"name": "John", "committee": "ECOSOC", "allotment": "Algeria", "email": "myEmail@outlook.com"},
    {"name": "John", "committee": "ECOSOC", "allotment": "Algeria", "email": "myEmail@snuchennai.edu.in"},
]

obj_recipients = [MySchema(**recipient) for recipient in recipients]
for recipient in obj_recipients:
    print("Hash:", recipient.hash_string)


automailer = AutoMailer(
    sender_email="myEmail@gmail.com",
    password="myPass",
    provider="gmail",
    session_name="test"
)

print("Mailer object created")

automailer.send_emails(
    recipients=obj_recipients,
    email_field="email",
    template=template
)
