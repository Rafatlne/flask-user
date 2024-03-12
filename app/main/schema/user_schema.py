from flask_restx import Namespace
from marshmallow import fields, validate, validates, ValidationError
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.main.model.models import Role, Contact, UserInfo


class UserDto:
    """Data Transfer object for User"""
    api = Namespace("users", description="User related operations")


class RoleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Role
        load_instance = True


class ContactSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Contact
        load_instance = True


class UserInfoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserInfo
        include_relationships = True
        load_instance = True
        include_fk = True
        exclude = ["password_hash", "about_me", "last_seen", "timestamp", "token", "token_expiration"]

    contact = fields.Nested(ContactSchema)
    role = fields.Nested(RoleSchema)

    phone = fields.String(required=True, validate=validate.Length(max=15))
    address = fields.String(required=True, validate=validate.Length(max=100))
    city = fields.String(required=True, validate=validate.Length(max=100))
    country = fields.String(required=True, validate=validate.Length(max=50))
    role_id = fields.Integer(required=True, load_only=True)
    username = fields.String(required=True)
    password = fields.String(required=True, load_only=True)

    # Custom validation for role_id
    @validates("role_id")
    def validate_role_id(self, value):
        if not Role.query.get(value):
            raise ValidationError("Invalid role_id")

    @validates('username')
    def validate_username_unique(self, value):
        existing_user = UserInfo.query.filter_by(username=value).first()

        if existing_user:
            raise ValidationError('Username already exists. Please choose a different one.')

        if len(value) < 3 or len(value) > 64:
            raise ValidationError('Username must be between 3 and 64 characters long')

        return value

