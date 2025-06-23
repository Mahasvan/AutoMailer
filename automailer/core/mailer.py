import smtplib
import re
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import json
from typing import Optional, Any
from automailer.core.template import TemplateEngine
from automailer.session_management.session_manager import SessionManager
from automailer.utils.logger import logger

class MailSender:
    def __init__(self, sender_email: str, password: str, provider: str = "gmail") -> None:
        if not self._validate_email(sender_email):
            logger.error(f"Invalid email address: {sender_email}")
            raise ValueError("Invalid email address format.")
        self.sender_email = sender_email
        self.password = password
        self.smtp_server, self.smtp_port = self._get_settings(provider)
        logger.info(f"MailSender initialized for {sender_email} using {provider} provider.")

    def _get_settings(self, provider: str) -> tuple[str, int]:
        settings_path = os.path.join(os.path.dirname(__file__), "settings.json")
        with open(settings_path, 'r') as f:
            settings: dict[str, list[Any]] = json.load(f)

        if provider not in settings:
            logger.error(f"Provider '{provider}' not found in settings.")
            raise ValueError("Invalid provider.")
        return tuple(settings[provider])  # type: ignore

    #check email format using regex
    def _validate_email(self, email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def send_individual_mail(
        self,
        to_email: str,
        subject: str,
        text_content: Optional[str] = None,
        html_content: Optional[str] = None,
        attachment_paths: Optional[list[str]] = None,
        cc: Optional[list[str]] = None,
        bcc: Optional[list[str]] = None,
    ) -> bool:

        if not self._validate_email(to_email):
            logger.error(f"Invalid recipient email address: {to_email}")
            raise ValueError("Invalid recipient email address format.")

        if not text_content and not html_content:
            logger.warning("Attempted to send an email with no content.")
            raise ValueError("At least one content type must be provided.")

        msg = MIMEMultipart("alternative")
        msg["From"] = self.sender_email
        msg["To"] = to_email
        msg["Subject"] = subject
        if cc:
            msg["Cc"] = ", ".join(cc)

        if text_content:
            msg.attach(MIMEText(text_content, "plain"))
        if html_content:
            msg.attach(MIMEText(html_content, "html"))

        if attachment_paths:
            for file_path in attachment_paths:
                try:
                    with open(file_path, "rb") as f:
                        part = MIMEApplication(f.read(), Name=os.path.basename(file_path))
                        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                        msg.attach(part)
                except Exception as e:
                    logger.warning(f"Couldn't attach file '{file_path}': {e}")
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
                logger.info(f"Email sent to {to_email}")
                return True

        except Exception as e:
            logger.error(f"Couldn't send email to {to_email}: {e}")
            return False

    def send_bulk_mail(
        self,
        recipients: list[dict[str, str]],
        template: TemplateEngine,
        attachment_paths: Optional[list[str]] = None,
        cc: Optional[list[str]] = None,
        bcc: Optional[list[str]] = None,
        session_manager: Optional[SessionManager] = None
    ) -> None:
        if not template.text and not template.html:
            logger.error("Both text and HTML templates are missing.")
            raise ValueError("At least one template must be provided.")

        for row in recipients:
            to_email = row["email"]
            subject = template.render_subject(row)
            text = template.render_text(row)
            html = template.render_html(row)

            try:
                sent = self.send_individual_mail(
                    to_email=to_email,
                    subject=subject,
                    text_content=text,
                    html_content=html,
                    attachment_paths=attachment_paths,
                    cc=cc,
                    bcc=bcc
                )
            except ValueError as e:
                logger.error(f"Error sending email to {to_email}: {e}")
                continue

            if sent and session_manager:
                session_manager.add_recipient(row)

            if not sent:
                logger.warning(f"Couldn't send email to {to_email}.")
