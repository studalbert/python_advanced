import csv
import datetime

from sqlalchemy import func, extract
from flask import Flask, jsonify, abort, request
from sqlalchemy.orm import joinedload

from hw_models import Base, engine, session, Book, ReceivingBook, Student


app = Flask(__name__)


@app.before_request
def before_request_func():
    Base.metadata.create_all(engine)


@app.route("/books", methods=["GET"])
def get_all_books():
    books = session.query(Book).all()
    books_list = [book.to_json() for book in books]
    return jsonify(books_list=books_list), 200


@app.route("/debtors", methods=["GET"])
def get_all_debtors():
    debtors = (
        session.query(ReceivingBook.student_id)
        .filter(
            ReceivingBook.count_date_with_book > 14,
            ReceivingBook.date_of_return == None,
        )
        .all()
    )
    debtors_id = [debtor[0] for debtor in debtors]
    students = session.query(Student).filter(Student.id.in_(debtors_id)).all()
    students_list = [student.to_json() for student in students]
    return jsonify(students_list=students_list), 200


@app.route("/givebooks", methods=["POST"])
def give_book():
    book_id = request.form.get("book_id", type=int)
    student_id = request.form.get("student_id", type=int)
    date_of_issue = datetime.datetime.now()
    new_receiving_book = ReceivingBook(
        book_id=book_id, student_id=student_id, date_of_issue=date_of_issue
    )
    session.add(new_receiving_book)
    session.commit()
    return "Книга успешно выдана", 200


@app.route("/returnbooks", methods=["POST"])
def return_book():
    book_id = request.form.get("book_id", type=int)
    student_id = request.form.get("student_id", type=int)
    book = (
        session.query(ReceivingBook)
        .filter(
            ReceivingBook.book_id == book_id, ReceivingBook.student_id == student_id
        )
        .one_or_none()
    )
    if book:
        book.date_of_return = datetime.datetime.now()
        session.commit()
        return "Книга успешно возвращена", 200
    else:
        return "В базе нет таких данных", 400


@app.route("/books", methods=["POST"])
def book_by_name():
    name = request.form.get("name", type=str)
    books = session.query(Book).filter(Book.name.ilike(f"%{name}%")).all()
    books_list = [book.to_json() for book in books]
    return jsonify(books_list=books_list), 200


@app.route("/books/<int:author_id>", methods=["GET"])
def books_count(author_id):
    books_cnt = (
        session.query(func.sum(Book.count)).filter(Book.author_id == author_id).scalar()
    )
    return jsonify(result=books_cnt), 200


@app.route("/unreadbooks/<int:student_id>", methods=["GET"])
def get_unread_books(student_id):
    books_q = (
        session.query(ReceivingBook.book_id, Book.name, Book.author_id)
        .join(Book)  # Явное соединение с таблицей Book
        .filter(ReceivingBook.student_id == student_id)
        .subquery()
    )
    unread_books = (
        session.query(Book)
        .filter(
            Book.author_id.in_(session.query(books_q.c.author_id)),
            Book.id.notin_(session.query(books_q.c.book_id)),
        )
        .all()
    )
    books_list = [book.to_json() for book in unread_books]
    return jsonify(unread_books=books_list), 200


@app.route("/averagecount", methods=["GET"])
def average_count():
    now = datetime.datetime.now()
    count_books = (
        session.query(ReceivingBook.book_id)
        .filter(
            extract("year", ReceivingBook.date_of_issue) == now.year,
            extract("month", ReceivingBook.date_of_issue) == now.month,
        )
        .count()
    )
    count_students = (
        session.query(ReceivingBook.student_id.distinct())
        .filter(
            extract("year", ReceivingBook.date_of_issue) == now.year,
            extract("month", ReceivingBook.date_of_issue) == now.month,
        )
        .count()
    )
    return jsonify(average_count=count_books / count_students), 200


@app.route("/mostpopular", methods=["GET"])
def most_popular_book():
    sq = (
        session.query(ReceivingBook.book_id, func.count().label("cnt"))
        .join(Student, ReceivingBook.student_id == Student.id)
        .filter(Student.average_score > 4.0)
        .group_by(ReceivingBook.book_id)
        .order_by(func.count().desc())
        .limit(1)
        .subquery()
    )
    res = session.query(Book).filter(Book.id == sq.c.book_id).one_or_none()
    if res:
        return jsonify(most_popular_book=res.to_json()), 200
    else:
        return jsonify({"message": "No popular book found"}), 404


@app.route("/topstudents", methods=["GET"])
def most_reading_students():
    now = datetime.datetime.now()
    top_students = (
        session.query(ReceivingBook.student_id, func.count(), Student)
        .filter(
            ReceivingBook.student_id == Student.id,
            extract("year", ReceivingBook.date_of_issue) == now.year,
        )
        .group_by(ReceivingBook.student_id)
        .order_by(func.count())
        .limit(10)
        .all()
    )
    students_list = [student[2].to_json() for student in top_students]
    return jsonify(students_list=students_list), 200


@app.route("/studentsinsert/<path:file_path>")
def insert_students(file_path):
    file_name = file_path
    with open(file_name, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")
        res_lst = []
        for row in reader:
            name = row["name"]
            surname = row["surname"]
            phone = row["phone"]
            email = row["email"]
            average_score = float(row["average_score"])
            scholarship = bool(row["scholarship"])
            res_lst.append(
                {
                    "name": name,
                    "surname": surname,
                    "phone": phone,
                    "email": email,
                    "average_score": average_score,
                    "scholarship": scholarship,
                }
            )
    session.bulk_insert_mappings(Student, res_lst)
    # session.add(
    #     Student(
    #         name=name,
    #         surname=surname,
    #         phone=phone,
    #         email=email,
    #         average_score=average_score,
    #         scholarship=scholarship,
    #     )
    # )
    session.commit()
    return "Студенты успешно добавлены", 201


if __name__ == "__main__":
    app.run(debug=True)
