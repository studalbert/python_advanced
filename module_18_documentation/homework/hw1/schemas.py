from marshmallow import post_load, validates
from flasgger import Schema, fields, ValidationError
from models import get_book_by_title, Book, Author


class AuthorSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)

    @post_load
    def create_author(self, data: dict, **kwargs) -> Book:
        return Author(**data)


class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    author = fields.Nested(AuthorSchema, required=True)

    @validates("title")
    def validate_title(self, title: str) -> None:
        if get_book_by_title(title) is not None:
            raise ValidationError(
                'Book with title "{title}" already exists, '
                "please use a different title.".format(title=title)
            )

    @post_load
    def create_book(self, data: dict, **kwargs) -> Book:
        return Book(**data)
