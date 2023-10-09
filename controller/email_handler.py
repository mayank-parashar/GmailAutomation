from servicer.constants import Action
from servicer.email_service import EmailService
import database.queries.email as email_queries
from servicer.rule_engine import RuleEngine


class EmailServiceHandler:
    def __init__(self):
        self.email_service = EmailService()
        self.rule_engine = RuleEngine()

    def fetch_and_save_email(self):
        for email in self.email_service.fetch_emails():
            #  Todo: we can do bulk save here
            email_queries.create(email)

    def execute_email_actions(self, action: Action, rules_dict):
        filters = self.rule_engine.generate_filters(rules_dict)
        collection_predicate = self.rule_engine.get_collection_predicate(rules_dict)
        chunk_size = 10
        message_id_list = []
        for email in email_queries.stream_message_id_email(filters, collection_predicate):
            print(email.message_id)
            if len(message_id_list) == chunk_size:
                # todo: running in small chunk so that in future it will be easy to move to bulk execute functionality
                self.email_service.execute_action(action, message_id_list)
                message_id_list = []
            message_id_list.append(email.message_id)
        else:
            self.email_service.execute_action(action, message_id_list)


