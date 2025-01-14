import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Float,
    Text,
    Date,
    Boolean,
    func,
)
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from sqlalchemy.ext.hybrid import hybrid_property


engine = create_engine("sqlite:///hw20.db")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    count = Column(Integer, default=1)
    release_date = Column(Date, nullable=False)
    author_id = Column(Integer, nullable=False)

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    surname = Column(Text, nullable=False)


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    surname = Column(Text, nullable=False)
    phone = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    average_score = Column(Float, nullable=False)
    scholarship = Column(Boolean, nullable=False)

    @classmethod
    def students_who_have_scholarship(cls):
        students = session.query(cls).filter(cls.scholarship == True).all()
        return students

    @classmethod
    def students_with_higher_score(cls, score):
        students = session.query(cls).filter(cls.average_score > score).all()
        return students

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ReceivingBook(Base):
    __tablename__ = "receiving_books"

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, nullable=False)
    student_id = Column(Integer, nullable=False)
    date_of_issue = Column(DateTime, nullable=False)
    date_of_return = Column(DateTime)

    @hybrid_property
    def count_date_with_book(self):
        if not self.date_of_return:
            today = datetime.datetime.now()
            diff = (today - self.date_of_issue).days
            return diff
        else:
            diff = (self.date_of_return - self.date_of_issue).days
            return diff

    @count_date_with_book.expression
    def count_date_with_book(cls):
        return func.julianday(
            func.ifnull(cls.date_of_return, func.now())
        ) - func.julianday(cls.date_of_issue)


Base.metadata.create_all(engine)
