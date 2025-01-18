import datetime
import re

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
    ForeignKey,
    extract,
    event,
)
from sqlalchemy.orm import (
    sessionmaker,
    declarative_base,
    relationship,
    backref,
    joinedload,
)
from sqlalchemy import create_engine
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.associationproxy import association_proxy

engine = create_engine("sqlite:///hw21.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    surname = Column(Text, nullable=False)


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    count = Column(Integer, default=1)
    release_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    author = relationship(
        "Author", backref=backref("books", cascade="all, delete-orphan", lazy="select")
    )
    students = relationship("ReceivingBook", back_populates="book")

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    surname = Column(Text, nullable=False)
    phone = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    average_score = Column(Float, nullable=False)
    scholarship = Column(Boolean, nullable=False)
    receiving_books = relationship("ReceivingBook", back_populates="student")
    books = association_proxy("receiving_books", "book")

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

    book_id = Column(Integer, ForeignKey("books.id"), primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"), primary_key=True)
    date_of_issue = Column(DateTime, nullable=False, default=datetime.datetime.now())
    date_of_return = Column(DateTime)
    student = relationship("Student", back_populates="receiving_books")
    book = relationship("Book", back_populates="students")

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


@event.listens_for(Student, "before_insert")
def before_insert(mapper, connection, target):
    print(target.phone)
    if not re.fullmatch(r"\+7\(9\d{2}\)-\d{3}-\d{2}-\d{2}", target.phone):
        raise ValueError("phone format is invalid.")


def insert_data():
    authors = [
        Author(name="Александр", surname="Пушкин"),
        Author(name="Лев", surname="Толстой"),
        Author(name="Михаил", surname="Булгаков"),
    ]
    authors[0].books.extend(
        [
            Book(
                name="Капитанская дочка",
                count=5,
                release_date=datetime.date(1836, 1, 1),
            ),
            Book(
                name="Евгений Онегин", count=3, release_date=datetime.date(1838, 1, 1)
            ),
        ]
    )
    authors[1].books.extend(
        [
            Book(name="Война и мир", count=10, release_date=datetime.date(1867, 1, 1)),
            Book(name="Анна Каренина", count=7, release_date=datetime.date(1877, 1, 1)),
        ]
    )
    authors[2].books.extend(
        [
            Book(name="Морфий", count=5, release_date=datetime.date(1926, 1, 1)),
            Book(
                name="Собачье сердце", count=3, release_date=datetime.date(1925, 1, 1)
            ),
        ]
    )

    students = [
        Student(
            name="Nik",
            surname="1",
            phone="2",
            email="3",
            average_score=4.5,
            scholarship=True,
        ),
        Student(
            name="Vlad",
            surname="1",
            phone="2",
            email="3",
            average_score=4,
            scholarship=True,
        ),
    ]
    session.add_all(authors)
    session.add_all(students)
    session.commit()


def give_me_book():
    nikita = session.query(Student).filter(Student.name == "Nik").one()
    vlad = session.query(Student).filter(Student.name == "Vlad").one()
    books_to_nik = (
        session.query(Book)
        .filter(Author.surname == "Толстой", Author.id == Book.author_id)
        .all()
    )
    books_to_vlad = session.query(Book).filter(Book.id.in_([1, 3, 4])).all()

    for book in books_to_nik:
        receiving_book = ReceivingBook(student=nikita, book=book)
        session.add(receiving_book)

    for book in books_to_vlad:
        receiving_book = ReceivingBook(student=vlad, book=book)
        session.add(receiving_book)

    session.commit()


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    check_exist = session.query(Author).all()
    if not check_exist:
        insert_data()
        give_me_book()
