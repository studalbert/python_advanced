import datetime

from flask import Flask, jsonify, abort, request
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


if __name__ == "__main__":
    app.run(debug=True)
