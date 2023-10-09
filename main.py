from apis.app import app
from controller.email_handler import EmailServiceHandler
from servicer.constants import Action
from servicer.email_service import EmailService

if __name__ == "__main__":
    EmailServiceHandler().fetch_and_save_email()
    EmailServiceHandler().execute_email_actions(Action.MOVE_INBOX, None)
    # app.run()
