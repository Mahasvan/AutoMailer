from automailer.core.mailer import MailSender
from automailer.core.template import TemplateEngine, TemplateModel
from automailer.session_management.session_manager import SessionManager
from typing import List, Dict, Optional
from automailer.utils.logger import logger

class AutoMailer:
    def __init__(self, sender_email: str, password: str, provider: str, session_name: str):
        logger.info(f"Initializing AutoMailer for {sender_email} with provider {provider} and session '{session_name}'")
        self.mailer = MailSender(sender_email, password, provider)
        self.session_manager = SessionManager(session_name)

    def send_emails(
        self,
        recipients: List[List[str]], # List[email addresses of each email]
        data: List[TemplateModel], # Variable replacements - same length as recipients
        template: TemplateEngine,
        attachment_paths,
        cc,
        bcc):
    
        logger.info(f"Preparing to send emails to {len(recipients)} recipients.")
        
        # todo: fix this stuff
        
        unsent = self.session_manager._filter_unsent_recipients(self.session_manager.get_current_session_id(), recipients)

        if not unsent:
            logger.info("All recipients already emailed.")
            return
    
        for rec_data in data:
            template.render(rec_data)

        self.mailer.send_bulk_mail(
            recipients=unsent,
            template=template,
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
