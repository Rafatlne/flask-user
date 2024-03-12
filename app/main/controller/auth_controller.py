from flask import jsonify
from flask_restx import Resource

from ..model.models import db
from ..schema.auth_schema import AuthDto
from ..util.auth import basic_auth, token_auth

api = AuthDto.api


@api.route("/")
class AuthController(Resource):

    @basic_auth.login_required
    @api.doc(description='Authenticate and get a token', security='Basic Auth')
    def post(self):
        """Authenticate and get a token"""
        token = basic_auth.current_user().get_token(expires_in=86400)
        db.session.commit()
        return jsonify({"token": token})

    @token_auth.login_required
    @api.doc(description='Revoke token')
    def delete(self):
        """Revoke token"""
        token_auth.current_user().revoke_token()
        db.session.commit()
        return '', 204
