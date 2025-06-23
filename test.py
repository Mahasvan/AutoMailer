from automailer import AutoMailer
from automailer import TemplateModel, TemplateEngine



with open("body.txt", "r") as f:
    body = f.read()

print("Body text loaded successfully.")
# print(body)

t = TemplateEngine(body_text=body)


recipients1 = [
    # fields = MyFields(name="John Doe", committee="ECOSOC", allotment="Algeria")
    {"name": "John", "committee": "ECOSOC", "allotment": "Algeria"},
    {"name": "Alice", "committee": "UNICEF", "allotment": "USA"},
    {"name": "Bob", "committee": "WHO", "allotment": "Canada"}
    ]


automailer1 = AutoMailer(
     sender_email="sender@gmail.com",
     password="password",
     provider="gmail",
     session_name="test1"
 )

class MySchema(TemplateModel):
    name: str
    committee: str
    allotment: str

input = []
for row in recipients1:
    input.append(MySchema(name=row["name"], committee=row["committee"], allotment=row["allotment"]))

automailer1.send_emails(
    recipients=input, #or recipients
    