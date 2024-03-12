from flask_restx import Namespace
from marshmallow import Schema, fields, validate, ValidationError, validates

from app.main.service.users_json_service import get_object


class JsonContactSchema(Schema):
    id = fields.Integer(dump_only=True)
    phone = fields.String(validate=validate.Length(max=15))
    address = fields.String(validate=validate.Length(max=100))
    city = fields.String(validate=validate.Length(max=50))
    country = fields.String(validate=validate.Length(max=50))


class JsonRoleSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(validate=validate.Length(max=50))


class JsonUserInfoSchema(Schema):
    id = fields.Integer(dump_only=True)
    first_name = fields.String(validate=validate.Length(max=50))
    last_name = fields.String(validate=validate.Length(max=50))
    active = fields.Boolean()
    company = fields.String(validate=validate.Length(max=100))
    sex = fields.String(validate=validate.OneOf(['M', 'F']))
    contact = fields.Nested(JsonContactSchema, dump_only=True)
    role = fields.Nested(JsonRoleSchema, dump_only=True)
    role_id = fields.Integer(required=True)
    phone = fields.String(required=True, validate=validate.Length(max=15))
    address = fields.String(required=True, validate=validate.Length(max=100))
    city = fields.String(required=True, validate=validate.Length(max=100))
    country = fields.String(required=True, validate=validate.Length(max=50))

    # Custom validation for role_id
    @validates("role_id")
    def validate_role_id(self, value):
        if not get_object(value, "roles"):
            raise ValidationError("Invalid role_id")


class JsonUserDto:
    """Data Transfer object for User"""
    api = Namespace("users-json", description="Users Json related operations")