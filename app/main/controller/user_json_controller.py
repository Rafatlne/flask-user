from flask import request
from flask_restx import Resource, fields
from marshmallow import ValidationError

from ..schema.json_user_schema import JsonUserDto, JsonUserInfoSchema
from ..service.users_json_service import (
    get_all_users,
    get_user_details,
    update_user,
    delete_user,
    create_user,
    get_search_result,
)
from ..util.auth import token_auth

api = JsonUserDto.api
json_userinfo_schema = JsonUserInfoSchema()
json_userinfos_schema = JsonUserInfoSchema(many=True)

contact_model = api.model(
    "JsonContact",
    {
        "id": fields.Integer(description="The role ID", example=1),
        "phone": fields.String(
            description="The user's phone number", example="123456789"
        ),
        "address": fields.String(
            description="The user's address", example="123 Main St"
        ),
        "city": fields.String(description="The user's city", example="New York"),
        "country": fields.String(description="The user's country", example="USA"),
    },
)

role_model = api.model(
    "JsonRole",
    {
        "id": fields.Integer(description="The role ID", example=1),
        "name": fields.String(description="The role name", example="Admin"),
    },
)

user_model = api.model(
    "JsonUser",
    {
        "id": fields.Integer(description="The user ID", example=1),
        "first_name": fields.String(
            description="The user's first name", example="John"
        ),
        "last_name": fields.String(description="The user's last name", example="Doe"),
        "active": fields.Boolean(
            description="Whether the user is active or not", example=True
        ),
        "company": fields.String(description="The user's company", example="ABC Inc."),
        "sex": fields.String(
            description="The user's gender", enum=["M", "F"], example="M"
        ),
        "contact": fields.Nested(
            contact_model, description="The user's contact information"
        ),
        "role": fields.Nested(role_model, description="The user's role information"),
        "phone": fields.String(
            description="The user's phone number", example="123456789"
        ),
        "address": fields.String(
            description="The user's address", example="123 Main St"
        ),
        "city": fields.String(description="The user's city", example="New York"),
        "country": fields.String(description="The user's country", example="USA"),
    },
)

user_post_model = api.model(
    "JsonUserPostModel",
    {
        "first_name": fields.String(
            description="The user's first name", example="John"
        ),
        "last_name": fields.String(description="The user's last name", example="Doe"),
        "active": fields.Boolean(
            description="Whether the user is active or not", example=True
        ),
        "company": fields.String(description="The user's company", example="ABC Inc."),
        "sex": fields.String(
            description="The user's gender", enum=["M", "F"], example="M"
        ),
        "role_id": fields.Integer(description="The ID of user's role", example=1),
        "phone": fields.String(
            description="The user's phone number", example="123456789"
        ),
        "address": fields.String(
            description="The user's address", example="123 Main St"
        ),
        "city": fields.String(description="The user's city", example="New York"),
        "country": fields.String(description="The user's country", example="USA"),
    },
)

search_model = api.model(
    "SearchModel",
    {
        "query": fields.String(
            required=True, description="Search query", example="Any text"
        )
    },
)


@api.route("/")
class JsonUserList(Resource):
    @token_auth.login_required
    @api.doc("list_users")
    @api.response(200, "Success", [user_model])
    @api.response(400, "Validation Error")
    def get(self):
        """List all users from JSON file"""
        return get_all_users()

    @api.doc("create_user")
    @api.expect(user_post_model, validate=True)
    @api.response(201, "User created", user_model)
    @api.response(400, "Validation Error")
    @token_auth.login_required
    def post(self):
        """Save a new user in JSON file"""
        user = request.json
        try:
            json_userinfo_schema.load(user)
        except ValidationError as err:
            return err.messages, 400

        return create_user(user)


@api.route("/<int:id>/")
@api.param("id", "The user identifier")
class JsonUser(Resource):
    @api.doc("get_user")
    @api.response(200, "Success", user_model)
    @api.response(404, "User not found")
    @token_auth.login_required
    def get(self, id):
        """Get a user by ID from JSON file"""
        return get_user_details(id)

    @api.doc("update_user")
    @token_auth.login_required
    @api.expect(user_post_model, validate=True)
    @api.response(200, "User updated", user_model)
    @api.response(400, "Validation Error")
    @api.response(404, "User not found")
    def put(self, id):
        """Update a user by ID from JSON file"""
        user_data = request.json
        try:
            json_userinfo_schema.load(user_data)
        except ValidationError as err:
            return err.messages, 400

        return update_user(id, user_data)

    @api.doc("delete_user")
    @token_auth.login_required
    @api.response(204, "User deleted")
    @api.response(404, "User not found")
    def delete(self, id):
        """Delete a user by ID from JSON file"""
        return delete_user(id)


@api.route("/search/")
class SearchUsers(Resource):
    @api.doc(
        params={
            "query": {
                "description": "Search users by query",
                "type": "string",
                "default": "Manager",
            }
        }
    )
    @token_auth.login_required
    @api.response(200, "Success", [user_model])
    @api.response(400, "Please provide a search query")
    def get(self):
        """Search users based on the provided query."""
        query = request.args.get("query")
        if query:
            return get_search_result(query)

        return {"message": "Please provide a search query"}, 400
