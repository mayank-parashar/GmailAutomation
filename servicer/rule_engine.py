import json

from database.models.email import Email
from database.queries.email import stream_email
from servicer.constants import ValidRuleFieldName, InternalPredicates
from servicer.struct import Rule, Rules
from utils import convert_datetime


class RuleEngine:
    def __init__(self):
        rules_dict = json.load(open("./rules.json"))
        self.rules: Rules = Rules.model_validate(rules_dict)

    def get_collection_predicate(self, rules_dict=None):
        rules_obj = Rules.model_validate(rules_dict) if rules_dict is not None else self.rules
        return rules_obj.predicates

    def generate_filters(self, rules_dict=None):
        filter_conditions = []
        rules_obj = Rules.model_validate(rules_dict) if rules_dict is not None else self.rules
        # can be handle in better way to reduce redundancy
        for rule in rules_obj.rules:
            if rule.field_name == ValidRuleFieldName.FROM_ADDRESS:
                if rule.predicates == InternalPredicates.contains:
                    filter_conditions.append(Email.from_address.contains(rule.value))
                elif rule.predicates == InternalPredicates.not_equals:
                    filter_conditions.append(Email.from_address != rule.value)
                else:
                    filter_conditions.append(Email.from_address == rule.value)

            if rule.field_name == ValidRuleFieldName.TO_ADDRESS:
                if rule.predicates == InternalPredicates.contains:
                    filter_conditions.append(Email.to_address.contains(rule.value))
                elif rule.predicates == InternalPredicates.not_equals:
                    filter_conditions.append(Email.to_address != rule.value)
                else:
                    filter_conditions.append(Email.to_address == rule.value)

            if rule.field_name == ValidRuleFieldName.SUBJECT:
                if rule.predicates == InternalPredicates.contains:
                    filter_conditions.append(Email.subject.contains(rule.value))
                elif rule.predicates == InternalPredicates.not_equals:
                    filter_conditions.append(Email.subject != rule.value)
                else:
                    filter_conditions.append(Email.subject == rule.value)

            if rule.field_name == ValidRuleFieldName.RECEIVED_DATE:
                received_date = convert_datetime(rule.value)
                if rule.predicates == InternalPredicates.less_than:
                    filter_conditions.append(Email.received_date < received_date)
                elif rule.predicates == InternalPredicates.greater_than:
                    filter_conditions.append(Email.received_date > received_date)
                elif rule.predicates == InternalPredicates.equals:
                    filter_conditions.append(Email.received_date == received_date)

        return filter_conditions




