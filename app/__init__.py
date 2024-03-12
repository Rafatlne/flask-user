from flask_restx import Api
from flask import Blueprint

from .main.controller.user_info_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.user_json_controller import api as user_json_ns


blueprint = Blueprint("api", __name__)


@blueprint.route("/")
def health_check():
    return {"message": "Application heath is ok."}, 200


authorizations = {
    "Bearer Auth": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "Enter the token with the `Bearer ` prefix, e.g. `Bearer abcde12345`. \n\n"
                       "To obtain a token, make a POST request to `/auth/` with the following JSON payload: \n\n"
                       "```\n"
                       "{\"username\": \"admin\", \"password\": \"admin@123\"}\n"
                       "```\n"
    }
}

api = Api(
    blueprint,
    title="FLASK USER STORAGE",
    version="1.0",
    description="A user flask api \n\n"
                "To obtain a token, make a POST request to `/auth/` with the following JSON payload: \n\n"
                "```\n"
                "{\"username\": \"admin\", \"password\": \"admin@123\"}\n"
                "```\n"
    ,
    authorizations=authorizations,
    security="Bearer Auth",
    doc="/doc/",
)

api.add_namespace(user_ns)
api.add_namespace(auth_ns)
api.add_namespace(user_json_ns)
