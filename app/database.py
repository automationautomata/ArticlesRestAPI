from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import constants
from app.models import Base

engine = create_engine(constants.DATABASE_URL, echo=True)

Base.metadata.create_all(engine, tables=Base.metadata.tables.values())

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
