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
    {"name": "John", "committee": "ECOSOC", "allotment": "Algeria", "email": "john@example.com"},
    {"name": "Alice", "committee": "UNICEF", "allotment": "USA", "email": "alice@example.com"},
    {"name": "Bob", "committee": "WHO", "allotment": "Canada", "email": "bob@example.com"},
]

obj_recipients = [MySchema(**recipient) for recipient in recipients]
for recipient in obj_recipients:
    print("Hash:", recipient.hash_string)


automailer = AutoMailer(
    sender_email="sender@gmail.com",
    password="app password",
    provider="gmail",
    session_name="test"
)

automailer.send_emails(
    recipients=recipients,
    schema=MySchema,
    template=template
)