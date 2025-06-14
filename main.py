from AutoMailer.core.mailer import MailSender
from AutoMailer.session_management.session_manager import SessionManager
from typing import List, Dict
from AutoMailer.core.template import Template


class AutoMailer:
    def __init__(self, sender_email: str, password: str, provider: str, db_path: str = "automailer.db"):
        #Mailer and session manager initialization
        self.mailer = MailSender(sender_email, password, provider)
        self.session_manager = SessionManager(db_path)

    # Start a new session and send emails to the recipients
    def start_send(
        self,
        recipients: List[Dict[str, str]],
        subject_template: str,
        text_template: str | None = None,
        html_template: str | None = None,
        attachment_paths: List[str] | None = None,
        cc: List[str] | None = None,
        bcc: List[str] | None = None
    ) -> int:
        session_id = self.session_manager.start_session(recipients)
        
        print(f"Session started with ID: {session_id}")
        template = Template(subject_template, text_template, html_template)

        self.mailer.send_bulk_mail(
            recipients=recipients,
            template=template,
            attachment_paths=attachment_paths,
            cc=cc,
            bcc=bcc,
            session_manager=self.session_manager,
            session_id=session_id
        )

        return session_id
    
    # Continue a session by sending emails to recipients that were not sent in the previous run
    def continue_session(
            self,
            session_id: int,
            subject_template: str,
            text_template: str = None,
            html_template: str = None,
            attachment_paths: List[str] = None,
            cc: List[str] = None,
            bcc: List[str] = None
    ) -> int:
        recipients = self.session_manager.continue_session(session_id)

        template = Template(subject_template, text_template, html_template)
        self.mailer.send_bulk_mail(
            recipients=recipients,
            template=template,
            attachment_paths=attachment_paths,
            cc=cc,
            bcc=bcc,
            session_manager=self.session_manager,
            session_id=session_id
        )
        if not recipients:
            print("No more recipients to send emails to in this session.")
        return session_id

    # Retry sending emails to recipients that failed in the previous run
    def retry_failed(
            self,
            session_id: int,
            subject_template: str,
            text_template: str = None,
            html_template: str = None,
            attachment_paths: List[str] = None,
            cc: List[str] = None,
            bcc: List[str] = None
    ) -> int:
        recipients = self.session_manager.retry_failed(session_id)
        template = Template(subject_template, text_template, html_template)
        self.mailer.send_bulk_mail(
            recipients=recipients,
            template=template,
            attachment_paths=attachment_paths,
            cc=cc,
            bcc=bcc,
            session_manager=self.session_manager,
            session_id=session_id
        )

        return session_id

    # Show all sessions
    def show_sessions(self) -> str:
        return self.session_manager.show_sessions()
    
