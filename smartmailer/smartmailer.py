from smartmailer.core.mailer import MailSender
from smartmailer.core.template import TemplateEngine
from smartmailer.session_management.session_manager import SessionManager
from typing import List
from smartmailer.utils.logger import logger
from smartmailer.utils.types import TemplateModelType


class AutoMailer:
    def __init__(self, sender_email: str, password: str, provider: str, session_name: str):
        logger.info(f"Initializing AutoMailer for {sender_email} with provider {provider} and session '{session_name}'")
        self.mailer = MailSender(sender_email, password, provider)
        self.session_manager = SessionManager(session_name)
        # print(f"AutoMailer initialized for {sender_email} with provider {provider} and session '{session_name}'")
        # print(f"{len(self.session_manager.get_sent_recipients())} recipients already sent in this session.")

    def send_emails(
        self,
        recipients: List[TemplateModelType],
        email_field: str,
        template: TemplateEngine,
        attachment_paths = None,
        cc = None,
        bcc= None,
        cc_field: str = "cc",
        bcc_field: str = "bcc",
        attachment_field: str = "attachments"
        ):
        all_attachment_paths = attachment_paths or []
        all_cc = cc or []
        all_bcc = bcc or []
    
        logger.info(f"Preparing to send emails to {len(recipients)} recipients.")

        
        sent = self.session_manager.filter_sent_recipients(recipients)
        print(f"{len(sent)} recipients already sent.")
        rendered_emails = []
        
        for recipient in recipients:
            if recipient in sent: 
                print(f"{recipient.__dict__[email_field]} already sent, skipping.")
                continue

            try:
                rendered = template.render(recipient)
                print("Rendered email:", rendered)

                rec_attachments = recipient.__dict__.get(attachment_field) or []
                rec_cc = recipient.__dict__.get(cc_field) or []
                rec_bcc = recipient.__dict__.get(bcc_field) or []

                combined_attachments = list(set(all_attachment_paths + rec_attachments))
                combined_cc = list(set(all_cc + rec_cc))
                combined_bcc = list(set(all_bcc + rec_bcc))

                rendered_email = {
                    "object": recipient,
                    "to_email": recipient.__dict__[email_field],
                    "subject": rendered.get("subject", ""),
                    "text_content": rendered.get("text", ""),
                    "html_content": rendered.get("html", None),
                    "attachments": combined_attachments,
                    "cc": combined_cc,
                    "bcc": combined_bcc
                }

                rendered_emails.append(rendered_email)
            except Exception as e:
                logger.error(f"Error rendering email for {recipient.__dict__[email_field]}: {e}")
                print(f"Error rendering email for {recipient.__dict__[email_field]}: {e}")

        self.mailer.send_bulk_mail(
            recipients=rendered_emails,
            attachment_paths=attachment_paths,
            cc=cc,
            bcc=bcc,
            session_manager=self.session_manager
        )

        logger.info('Completed sending emails.')
        print("Completed sending emails.")

    def show_sent(self):
        sent = self.session_manager.get_sent_recipients()
        logger.info(f"Fetched {len(sent)} sent recipients.")
        print("Sent Recipients:")
        for entry in sent:
            print(entry)