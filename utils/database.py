from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(
    "postgres://qimigqpctbbuom:5ac7371fd5d8d4daf5743c026d3915f986dadfbf9a717b2ba4f1ec95b8d7baea@ec2-23-21-136-232.compute-1.amazonaws.com:5432/d4ndcf7u2mpos1",
)

# engine = create_engine('sqlite:///location_rwas.db', convert_unicode=True)


def new_session():
    # engine = create_engine('sqlite:///location_rwas.db', convert_unicode=True)
    return scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine))


db_session = new_session()

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
