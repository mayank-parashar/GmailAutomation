from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models.email import Email  # do not remove it
from database.models.base import Base

engine = create_engine(f"sqlite:///email_service.db")
Base.metadata.create_all(bind=engine)


class DBSession(object):
    def __new__(cls):
        if not hasattr(cls, 'session'):
            Session = sessionmaker()
            Session.configure(bind=engine)
            cls.session = Session()
        return cls.session
