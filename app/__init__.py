from flask_restx import Api
from flask import Blueprint

from .main.controller.user_info_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.user_json_controller import api as user_json_ns


blueprint = Blueprint("api", __name__)


@blueprint.route("/")
def health_check():
    return {"message": "Application heath is ok."}, 200


authorizations = {"apikey": {"type": "apiKey", "in": "header", "name": "Authorization"}}

api = Api(
    blueprint,
    title="FLASK CONFIG STORAGE",
    version="1.0",
    description="a flask google storage connection api",
    # authorizations=authorizations,
    security="apikey",
    doc="/doc/",
)

api.add_namespace(user_ns)
api.add_namespace(auth_ns)
api.add_namespace(user_json_ns)
