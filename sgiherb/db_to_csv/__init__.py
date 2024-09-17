from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()
engine = create_engine("sqlite:///sgiherb.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
