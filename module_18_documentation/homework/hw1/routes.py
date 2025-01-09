from flask import Flask, request
from flask_restful import Api, Resource
from marshmallow import ValidationError

# from werkzeug.serving import WSGIRequestHandler
from models import (
    DATA,
    get_all_books,
    init_db,
    add_book,
    swag_from_json,
    get_book_by_id,
    update_book_by_id,
    delete_book_by_id,
    get_books_by_author,
    add_author,
    delete_author_by_id,
)

from schemas import BookSchema, AuthorSchema
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flasgger import APISpec, Swagger, swag_from

app = Flask(__name__)
api = Api(app)
spec = APISpec(
    title="BooksAPI",
    version="1.0.0",
    openapi_version="2.0",
    plugins=[
        FlaskPlugin(),
        MarshmallowPlugin(),
    ],
)


class BookList(Resource):
    @swag_from("yml_files/booklist_get.yml")
    def get(self) -> tuple[list[dict], int]:
        schema = BookSchema()
        return schema.dump(get_all_books(), many=True), 200

    @swag_from("yml_files/booklist_post.yml")
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
    @swag_from("yml_files/books_get.yml")
    def get(self, id: int):
        book = get_book_by_id(id)
        if book:
            schema = BookSchema()
            return schema.dump(book)
        else:
            return {"data": "Book not found"}, 404

    @swag_from("yml_files/books_put.yml")
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

    @swag_from("yml_files/books_delete.yml")
    def delete(self, id):
        try:
            delete_book_by_id(id)
            return {"data": "Book deleted succesfully"}, 204
        except ValueError:
            return {"data": "Resource not found."}, 404


class Authors(Resource):
    @swag_from_json("json_files/authors_get.json")
    def get(self, id):
        """This is an endpoint for obtaining the books list by author id"""
        schema = BookSchema()
        try:
            books = get_books_by_author(id)
            return schema.dump(books, many=True), 200
        except ValueError:
            return {"data": "Resource not found."}, 404

    @swag_from_json("json_files/authors_delete.json")
    def delete(self, id):
        """This is an endpoint for delete the author by id."""
        try:
            delete_author_by_id(id)
            return {"data": "the author was deleted succesfully"}, 204
        except ValueError:
            return {"data": "Resource not found."}, 404


class AuthorsCreate(Resource):
    @swag_from_json("json_files/authors_post.json")
    def post(self):
        """This is an endpoint for author creation."""
        data = request.json
        schema = AuthorSchema()
        try:
            author = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400
        author = add_author(author)
        return schema.dump(author), 201


template = spec.to_flasgger(
    app,
    definitions=[BookSchema],
)

swagger = Swagger(app, template=template)

api.add_resource(BookList, "/api/books")
api.add_resource(Books, "/api/books/<int:id>")
api.add_resource(Authors, "/api/authors/<int:id>")
api.add_resource(AuthorsCreate, "/api/authors")

if __name__ == "__main__":
    init_db(initial_records=DATA)
    # WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run(debug=True)
