from marshmallow import Schema, fields, validates, ValidationError, post_load


class CoffeeSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    origin = fields.String()
    intensifier = fields.String()
    notes = fields.List(fields.String())


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    has_sale = fields.Boolean()
    address = fields.Dict()
    coffee_id = fields.Integer()
    coffee = fields.Nested(CoffeeSchema, dump_only=True)
