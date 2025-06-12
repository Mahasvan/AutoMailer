import smtplib
import csv
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


class MailSender:
    def __init__(self, sender_email, password, provider="gmail"):
        #Sender credentials
        self.sender_email = sender_email
        self.password = password
        self.smtp_server, self.smtp_port = self._get_settings(provider)

    #Get the email client's server and port
    def _get_settings(self, provider):
        settings = {
            "gmail": ("smtp.gmail.com", 587),
            "outlook": ("smtp.office365.com", 587),
        }
        if provider not in settings:
            raise ValueError("Invalid provider.")
        return settings[provider]

    #Get a list of dictionaries as recipients data if user has a csv file with the data
    def load_csv_data(self, file_path):
        with open(file_path, newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            data = []
            for row in reader:
                email = row.get("email")
                if self._validate_email(email):
                    data.append(row)
                else:
                    print(f"Invalid email: {email}")
            return data

    #Check email ID format
    def _validate_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email)

    #Substitute the placeholders in the template with recipient data
    def _fill_template(self, template, row):
        for key, value in row.items():
            template = template.replace(f"{{{{{key}}}}}", value)
        return template

    #Sending the email
    def send_bulk_mail(self, recipients, subject_template, text_template=None,
        html_template=None, attachment_paths=None, cc=None, bcc=None):
        if not text_template and not html_template:
            raise ValueError("At least one template must be provided.")

        for row in recipients:
            to_email = row["email"]
            subject = self._fill_template(subject_template, row)
            text = self._fill_template(text_template, row) if text_template else None
            html = self._fill_template(html_template, row) if html_template else None

            msg = MIMEMultipart("alternative")
            msg["From"] = self.sender_email
            msg["To"] = to_email
            msg["Subject"] = subject
            if cc:
                msg["Cc"] = ", ".join(cc)

            #Email in plain text format
            if text:
                msg.attach(MIMEText(text, "plain"))
            #Email in HTML format
            if html:
                msg.attach(MIMEText(html, "html"))

            #Attachments (the path must be a raw string)
            if attachment_paths:
                for file_path in attachment_paths:
                    try:
                        with open(file_path, "rb") as f:
                            part = MIMEApplication(f.read(), Name=file_path)
                            part['Content-Disposition'] = f'attachment; filename="{file_path}"'
                            msg.attach(part)
                    except Exception as e:
                        print(f"Couldn't attach file {file_path}")

            try:
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.sender_email, self.password)
                    server.sendmail(
                        self.sender_email,
                        [to_email] + (cc or []) + (bcc or []),
                        msg.as_string()
                    )

                    #Message for successful email, must be replaced with database logic later
                    print(f"Email sent to {to_email}")
            except Exception as e:
                print(f"Couldn't send email to {to_email}")

