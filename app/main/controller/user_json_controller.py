from flask import request
from flask_restx import Resource
from marshmallow import ValidationError

from ..schema.json_user_schema import JsonUserDto, JsonUserInfoSchema
from ..service.users_json_service import (
    get_all_users,
    get_user_details,
    update_user,
    delete_user,
    create_user,
)
from ..util.auth import token_auth

api = JsonUserDto.api
json_userinfo_schema = JsonUserInfoSchema()
json_userinfos_schema = JsonUserInfoSchema(many=True)


@api.route("/")
class UserList(Resource):
    @token_auth.login_required
    @api.doc("list_users")
    def get(self):
        """List all users"""
        return get_all_users()

    @api.doc("create_user")
    @token_auth.login_required
    def post(self):
        """Create a new user"""
        user = request.json
        try:
            json_userinfo_schema.load(user)
        except ValidationError as err:
            return err.messages, 400

        return create_user(user)


@api.route("/<int:id>/")
@api.param("id", "The user identifier")
class User(Resource):
    @api.doc("get_user")
    @token_auth.login_required
    def get(self, id):
        """Get a user by ID"""
        return get_user_details(id)

    @api.doc("update_user")
    @token_auth.login_required
    def put(self, id):
        """Update a user by ID"""
        user_data = request.json
        try:
            json_userinfo_schema.load(user_data)
        except ValidationError as err:
            return err.messages, 400

        return update_user(id, user_data)

    @api.doc("delete_user")
    @token_auth.login_required
    def delete(self, id):
        """Delete a user by ID"""
        return delete_user(id)
