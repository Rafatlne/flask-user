from flask_restx import Resource

from ..model.models import UserInfo
from ..schema.user_schema import UserInfoSchema, UserDto
from ..util.auth import token_auth

api = UserDto.api
userinfo_schema = UserInfoSchema()
userinfos_schema = UserInfoSchema(many=True)


@api.route("/")
class UserInfoListController(Resource):

    @token_auth.login_required
    @api.doc('Get list of users')
    def get(self):
        """Get list of users"""
        userinfos = UserInfo.query.all()
        result = userinfos_schema.dump(userinfos)
        return result, 200


@api.route("/<int:id>/")
@api.param('id', 'The user identifier')
class UserInfoDetailsController(Resource):

    @token_auth.login_required
    @api.doc('Get a user by id')
    def get(self, id):
        """Get a user by id"""
        user = UserInfo.query.get(id)

        if not user:
            return {'message': 'User not found'}, 404

        return userinfo_schema.dump(user), 200
