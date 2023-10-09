from sqlalchemy import Column, String, DateTime, Integer, func, Index

from database.models.base import Base


class Email(Base):
    __tablename__ = "email"
    # id = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(String(24), nullable=False, index=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    from_address = Column('from', String(320), index=True)  # max length possible is 32 for gmail but might be
    to_address = Column('to', String(320), index=True)  # up to 320 for other service provider
    subject = Column(String(96), index=True)  # max length of subject possible is 96 for gmail
    received_date = Column(DateTime(timezone=True), index=True)
    email_body = Column(String)  # current requirement will probably need it
