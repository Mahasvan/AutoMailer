from AutoMailer import AutoMailer, MailSender, Template
import json
from pprint import pprint

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


recipients1 = [
    {"email": "alice@example.com", "name": "Alice"},
    {"email": "bob@example.com", "name": "Bob"}]

recipients2 = [
    {"email": "johndoe@example.com", "name": "John Doe"},
    {"email": "janedoe@example.com", "name": "Jane Doe"}
]

'''
recipients = [
    {"email": "alice@example.com", "name": "Alice"},
    {"email": "bob@example.com", "name": "Bob"}
]
'''

automailer1 = AutoMailer(
    sender_email="sender@gmail.com",
    password="password",
    provider="gmail",
    session_name="plsworksob10"
)

automailer2 = AutoMailer(
    sender_email="sender@gmail.com",
    password="password",
    provider="gmail",
    session_name="plsworksob20"
)

automailer1.send_emails(
    recipients=recipients1, #or recipients
    subject_template="Hello {{name}}",
    text_template="Hi {{name}}, this is a test email.",
    html_template="<p>Hi <b>{{name}}</b>, this is a test email.</p>")

import time; time.sleep(5)

automailer2.send_emails(
    recipients=recipients2, #or recipients
    subject_template="Greetings {{name}}",
    text_template="Hello {{name}}, this is another test email.",
    html_template="<p>Hello <b>{{name}}</b>, this is another test email.</p>")


automailer1.show_sent()
automailer2.show_sent()