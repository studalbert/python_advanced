from sqlalchemy import Column, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine

engine = create_engine("sqlite:///hw_22.db")
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = "users"
    email = Column(Text, primary_key=True)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
