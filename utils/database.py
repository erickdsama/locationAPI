from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///location_rwas.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class CRUD():
    def save(self):
        if self.id is None:
            db_session.add(self)
        return db_session.commit()

    def destroy(self):
        db_session.delete(self)
        return db_session.commit()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from models import Operator, Users, Devices, Locations, Requests
    Base.metadata.create_all(bind=engine)
