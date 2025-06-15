from AutoMailer.core.mailer import MailSender
from AutoMailer.core.template import Template
from AutoMailer.session_management.session_manager import SessionManager
from typing import List, Dict


class AutoMailer:
    def __init__(self, sender_email: str, password: str, provider: str, session_name: str):
        self.mailer = MailSender(sender_email, password, provider)
        self.session_manager = SessionManager(session_name)

    def send_emails(
        self,
        recipients: List[Dict[str, str]],
        subject_template: str,
        text_template: str = None,
        html_template: str = None,
        attachment_paths: List[str] = None,
        cc: List[str] = None,
        bcc: List[str] = None
    ):
        template = Template(subject_template, text_template, html_template)

        unsent = self.session_manager._filter_unsent_recipients(None, recipients)
        if not unsent:
            print("All recipients already emailed.")
            return

        self.mailer.send_bulk_mail(
            recipients=unsent,
            template=template,
            attachment_paths=attachment_paths,
            cc=cc,
            bcc=bcc,
            session_manager=self.session_manager
        )

        print("Completed sending emails.")

    def show_sent(self):
        sent = self.session_manager.get_sent_recipients()
        print("Sent Recipients:")
        for entry in sent:
            print(entry)
