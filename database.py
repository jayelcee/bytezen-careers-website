from sqlalchemy import create_engine, Column, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import os

DATABASE_URI = os.environ['DATABASE_URI']

engine = create_engine(DATABASE_URI, echo=True)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class Job(Base):
  __tablename__ = 'jobs'

  id = Column(Integer, primary_key=True)
  title = Column(String(250))
  location = Column(String(250))
  salary = Column(Numeric(10, 2))
  currency = Column(String(10))
  responsibilities = Column(String(2000))
  requirements = Column(String(2000))

# Function to initialize the database (create tables)
def init_db():
    Base.metadata.create_all(bind=engine)