import enum
GOOGLE_APIS_URL = "https://www.googleapis.com/auth/gmail"
EMAIL_SCOPE = [
    GOOGLE_APIS_URL + ".readonly",
    GOOGLE_APIS_URL + '.modify'
]


class Action(enum.Enum):
    MARK_READ = "READ"
    MARK_UNREAD = "UNREAD"
    MOVE_SPAM = "SPAM"
    MOVE_TRASH = "TRASH"
    MOVE_INBOX = "INBOX"


class InternalPredicates(enum.Enum):
    equals = "equals"
    contains = "contains"
    not_equals = "not_equals"
    less_than = "less_than"
    greater_than = "greater_than"


class PREDICATES(enum.Enum):
    AND = "and"
    ANY = "any"


class ValidRuleFieldName(enum.Enum):
    FROM_ADDRESS = "from_address"
    TO_ADDRESS = "to_address"
    SUBJECT = 'subject'
    RECEIVED_DATE = 'received_date'
    EMAIL_BODY = "email_body"
