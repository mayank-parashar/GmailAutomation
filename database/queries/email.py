from typing import Any

from sqlalchemy import or_, and_

from database.db import DBSession
from database.models.email import Email

from servicer.constants import PREDICATES
from servicer.struct import EmailData, Rules


def create(email_data: EmailData) -> Email:
    email = Email(
        message_id=email_data.message_id,
        from_address=email_data.from_address,
        to_address=email_data.to_address,
        subject=email_data.subject,
        received_date=email_data.received_date,
        email_body=email_data.email_body
    )
    DBSession().add(email)
    DBSession().commit()
    return email


def stream_email(filter_conditions: list[Any], collection_predicate: PREDICATES):
    if collection_predicate == PREDICATES.AND:
        query = DBSession().query(Email).filter(and_(*filter_conditions)).yield_per(1000)
    else:
        query = DBSession().query(Email).filter(or_(*filter_conditions)).yield_per(1000)
    for email in query:
        yield email


def stream_message_id_email(filter_conditions: list[Any], collection_predicate: PREDICATES):
    if collection_predicate == PREDICATES.AND:
        query = DBSession().query(Email.message_id.label('message_id')).filter(and_(*filter_conditions)).yield_per(1000)
    else:
        query = DBSession().query(Email.message_id.label('message_id')).filter(or_(*filter_conditions)).yield_per(1000)
    for email in query:
        yield email


#  Todo create email in database in bulk
# def create_bulk(){
#     DBSession.add()
# }
