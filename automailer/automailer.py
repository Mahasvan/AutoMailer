from automailer.core.mailer import MailSender
from automailer.core.template import TemplateEngine, TemplateModel
from automailer.session_management.session_manager import SessionManager
from typing import List, Dict, Optional, Type
from automailer.utils.logger import logger

class AutoMailer:
    def __init__(self, sender_email: str, password: str, provider: str, session_name: str):
        logger.info(f"Initializing AutoMailer for {sender_email} with provider {provider} and session '{session_name}'")
        self.mailer = MailSender(sender_email, password, provider)
        self.session_manager = SessionManager(session_name)

    def send_emails(
        self,
        recipients: List[Dict[str,str]],
        schema: Type[TemplateModel], 
        template: TemplateEngine,
        attachment_paths = None,
        cc = None,
        bcc= None):
    
        logger.info(f"Preparing to send emails to {len(recipients)} recipients.")

        unsent = self.session_manager._filter_unsent_recipients(self.session_manager.get_current_session_id(), recipients)

        if not unsent:
            logger.info("All recipients already emailed.")
            return
    
        rendered_emails = []
        for recipient in unsent:
            try:
                fields = schema(**recipient)
                rendered = template.render(fields)
                print("Rendered email:", rendered)

                rendered_email = {
                    "to_email": recipient["email"],
                    "subject": rendered.get("subject", ""),
                    "text_content": rendered.get("text", ""),
                    "html_content": rendered.get("html", None)
                }

                rendered_emails.append(rendered_email)
                self.session_manager.add_recipient(recipient)
            except Exception as e:
                logger.error(f"Error rendering email for {recipient['email']}: {e}")
                print(f"Error rendering email for {recipient['email']}: {e}")

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
