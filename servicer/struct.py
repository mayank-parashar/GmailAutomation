import datetime
from pydantic import BaseModel

from servicer.constants import PREDICATES, ValidRuleFieldName, InternalPredicates


class EmailData(BaseModel):
    message_id: str
    email_body: bytes
    received_date: datetime.datetime
    subject: str
    to_address: str
    from_address: str


class Rule(BaseModel):
    field_name: ValidRuleFieldName
    value: str
    predicates: InternalPredicates


class Rules(BaseModel):
    rules: list[Rule]
    predicates: PREDICATES
