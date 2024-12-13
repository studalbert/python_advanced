from flask import Flask, render_template, request
from typing import List
from flask_wtf.csrf import CSRFProtect
from models import init_db, get_all_books, DATA, save_books, BooksForm, get_author_func
from module_14_mvc.homework.models import book_id_view
import os
from dotenv import load_dotenv

load_dotenv()
app: Flask = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
csrf = CSRFProtect(app)


def _get_html_table_for_books(books: List[dict]) -> str:
    table = """
<table>
    <thead>
    <tr>
        <th>ID</td>
        <th>Title</td>
        <th>Author</td>
    </tr>
    </thead>
    <tbody>
        {books_rows}
    </tbody>
</table>
"""
    rows: str = ""
    for book in books:
        rows += "<tr><td>{id}</tb><td>{title}</tb><td>{author}</tb></tr>".format(
            id=book["id"],
            title=book["title"],
            author=book["author"],
        )
    return table.format(books_rows=rows)


@app.route("/books")
def all_books() -> str:
    return render_template(
        "index.html",
        books=get_all_books(),
    )


@app.route("/books/form", methods=["GET", "POST"])
def get_books_form() -> str:
    form = BooksForm()
    if request.method == "POST":
        if form.validate_on_submit():
            name, author = form.book_title.data, form.author_name.data
            save_books(name, author)
            return render_template(
                "index.html",
                books=get_all_books(),
            )

    elif request.method == "GET":
        return render_template("add_book.html", form=form)


@app.route("/books/<author>")
def get_author(author: str):
    return render_template("hw3.html", books=get_author_func(author))


@app.route("/books/<int:id>")
def view_counter(id: int):
    return render_template("hw4.html", books=book_id_view(id), id=id)


if __name__ == "__main__":
    init_db(DATA)
    app.run(debug=True)
