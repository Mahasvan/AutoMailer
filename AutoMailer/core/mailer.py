import smtplib
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import json
from template import Template
from session_management.session_manager import SessionManager

class MailSender:
    def __init__(self, sender_email: str, password: str, provider: str = "gmail") -> None:
        #Sender credentials
        self.sender_email = sender_email
        self.password = password
        self.smtp_server, self.smtp_port = self._get_settings(provider)

    #Get the email client's server and port
    def _get_settings(self, provider: str) -> tuple[str, int]:
        with open('settings.json', 'r') as f:
            settings = json.load(f)
            
        if provider not in settings:
            raise ValueError("Invalid provider.")
        return (settings[provider])

    #Check email ID format
    def _validate_email(self, email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email)

    #Sending the email
    def send_individual_mail(
        self,
        to_email: str,
        subject: str,
        text_content: str = None,
        html_content: str = None,
        attachment_paths: list[str] = None,
        cc: list[str] = None,
        bcc: list[str] = None) -> bool:
    
        if not text_content and not html_content:
            raise ValueError("At least one content type must be provided.")
        
        msg = MIMEMultipart("alternative")
        msg["From"] = self.sender_email
        msg["To"] = to_email
        msg["Subject"] = subject
        if cc:
            msg["Cc"] = ", ".join(cc)

        # Email in plain text format
        if text_content:
            msg.attach(MIMEText(text_content, "plain"))
        # Email in HTML format
        if html_content:
            msg.attach(MIMEText(html_content, "html"))

        # Attachments (the path must be a raw string)
        if attachment_paths:
            for file_path in attachment_paths:
                try:
                    with open(file_path, "rb") as f:
                        part = MIMEApplication(f.read(), Name=file_path)
                        part['Content-Disposition'] = f'attachment; filename="{file_path}"'
                        msg.attach(part)
                except Exception as e:
                    print(f"Couldn't attach file {file_path}: {e}")
                    return False

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.password)
                server.sendmail(
                    self.sender_email,
                    [to_email] + (cc or []) + (bcc or []),
                    msg.as_string()
                )
                print(f"Email sent to {to_email}")
                return True
            
        except Exception as e:
            print(f"Couldn't send email to {to_email}: {e}")
            return False


    def send_bulk_mail(
        self, 
        recipients: list[dict[str, str]], 
        template: Template,
        attachment_paths: list[str] = None, 
        cc: list[str] = None, 
        bcc: list[str] = None,
        session_manager: SessionManager = None,
        session_id: int = None
        ):
        
        if not template.text and not template.html:
            raise ValueError("At least one template must be provided.")
        
        for row in recipients:
            to_email = row["email"]
            subject = template.render_subject(row)
            text = template.render_text(row)
            html =  template.render_html(row)
           
            if session_manager:
                session_manager.update_status(row, session_id, "In Progress")

            sent = self.send_individual_mail(
                to_email=to_email,
                subject=subject,
                text_content=text,
                html_content=html,
                attachment_paths=attachment_paths,
                cc=cc,
                bcc=bcc,
                session_manager=session_manager
            )
            if sent and session_manager:
                session_manager.update_status(row, session_id, "Sent")
            
            if not sent and session_manager:
                session_manager.update_status(row, session_id, "Failed")