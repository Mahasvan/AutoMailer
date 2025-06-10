import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(sender,sender_pw, recipients, subject, text,html):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)


    msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))


    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, sender_pw)
            server.sendmail(sender, recipients, msg.as_string())

    except Exception as e:
        print(e)