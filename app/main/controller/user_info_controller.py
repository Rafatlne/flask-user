from flask import request
from flask_restx import Resource
from sqlalchemy import engine
from sqlalchemy.orm import sessionmaker, scoped_session

from ..model.models import UserInfo, db, Contact
from ..util.auth import token_auth
from ..util.user_dto import UserDto, UserInfoSchema

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
#
#     # @token_auth.login_required
#     @api.doc('Create a new user')
#     def post(self):
#         """Create a new user"""
#         data = request.json
#
#         sess = scoped_session(sessionmaker(bind=engine))
#         errors = userinfo_schema.validate(data, session=sess)
#         if errors:
#             return errors, 400
#
#         contact = Contact(
#             phone=data['phone'],
#             address=data['phone'],
#             city=data['city'],
#             country=data['country']
#         )
#
#         db.session.add(contact)
#         db.session.commit()
#         user = UserInfo(
#             first_name=data['first_name'],
#             last_name=data['last_name'],
#             active=data['active'],
#             company=data['company'],
#             sex=data['sex'],
#             username=data['username'],
#             role_id=data.pop('role_id'),
#             contact_id=contact.id
#         )
#
#         user.set_password(data['password'])
#         db.session.add(user)
#         db.session.commit()
#
#         return userinfo_schema.dump(user), 201
#
#
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
#
#     @token_auth.login_required
#     @api.doc('Delete a user by id')
#     def delete(self, id):
#         """Delete a user by id"""
#         user = UserInfo.query.get(id)
#
#         if not user:
#             return {'message': 'User not found'}, 404
#
#         db.session.delete(user)
#         db.session.commit()
#
#         return {'message': 'User deleted successfully'}, 204
