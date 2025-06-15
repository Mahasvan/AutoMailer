from AutoMailer.session_management.db import Database
from AutoMailer.session_management.session_manager import SessionManager
import json
from pprint import pprint
from AutoMailer.automailer import AutoMailer

# db = Database("test.db")

# try:
#     db.insert_recipient("First Recipient Hash")
#     db.insert_recipient("Second Recipient Hash")
# except:
#     print("Error inserting test recipients. They may already exist.")
# else:
#     print("Inserted test recipients.")

# print("Retrieving recipients:\n")
# pprint(db.get_sent_recipients())


# sm = SessionManager("TestSession")

# sm.add_recipient({"name": "John Doe"})
# sm.add_recipient({"name": "Jane Doe"})

# recipients = sm.get_sent_recipients()

# print("Sent recipients:")
# for recipient in recipients:
#     pprint(recipient)


recipients = [
    {"email": "johndoe@gmail.com", "name": "John Doe"},
    {"email": "janedoe@gmail.com", "name": "Jane Doe"}
]


automailer = AutoMailer(
    sender_email="sender@gmail.com",
    password="password",
    provider="gmail",
    session_name="testing1"
)

automailer.send_emails(
    recipients=recipients,
    subject_template="Hello {{name}}",
    text_template="Hi {{name}}, this is a test email.",
    html_template="<p>Hi <b>{{name}}</b>, this is a test email.</p>")

automailer.show_sent()