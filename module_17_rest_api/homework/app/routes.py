from flask import Flask, request
from flask_restful import Api, Resource
from marshmallow import ValidationError

from models import (
    DATA,
    get_all_books,
    init_db,
    add_book,
)
from module_17_rest_api.homework.app.models import (
    get_book_by_id,
    update_book_by_id,
    delete_book_by_id,
    get_books_by_author,
    add_author,
    delete_author_by_id,
)
from schemas import BookSchema, AuthorSchema

app = Flask(__name__)
api = Api(app)


class BookList(Resource):
    def get(self) -> tuple[list[dict], int]:
        schema = BookSchema()
        return schema.dump(get_all_books(), many=True), 200

    def post(self) -> tuple[dict, int]:
        data = request.json
        schema = BookSchema()
        try:
            book = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        book = add_book(book)
        return schema.dump(book), 201


class Books(Resource):
    def get(self, id: int):
        book = get_book_by_id(id)
        if book:
            schema = BookSchema()
            return schema.dump(book)
        else:
            return {"data": "Book not found"}, 404

    def put(self, id):
        data = request.json
        schema = BookSchema()
        try:
            book = schema.load(data)
            book.id = id
        except ValidationError as exc:
            return exc.messages, 400
        update_book_by_id(book)
        return schema.dump(get_book_by_id(id)), 200

    def delete(self, id):
        try:
            delete_book_by_id(id)
            return {"data": "Book deleted succesfully"}, 204
        except ValueError:
            return {"data": "Resource not found."}, 404


class Authors(Resource):
    def post(self):
        data = request.json
        schema = AuthorSchema()
        try:
            author = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400
        author = add_author(author)
        return schema.dump(author), 201

    def get(self, id):
        schema = BookSchema()
        try:
            books = get_books_by_author(id)
            return schema.dump(books, many=True), 200
        except ValueError:
            return {"data": "Resource not found."}, 404

    def delete(self, id):
        try:
            delete_author_by_id(id)
            return {"data": "the author was deleted succesfully"}, 204
        except ValueError:
            return {"data": "Resource not found."}, 404


api.add_resource(BookList, "/api/books")
api.add_resource(Books, "/api/books/<int:id>")
api.add_resource(Authors, "/api/authors", "/api/authors/<int:id>")

if __name__ == "__main__":
    init_db(initial_records=DATA)
    app.run(debug=True)
