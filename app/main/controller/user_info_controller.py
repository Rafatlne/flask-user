from flask_restx import Resource, fields

from ..model.models import UserInfo
from ..schema.user_schema import UserInfoSchema, UserDto
from ..util.auth import token_auth
from ..util.constant import RoleType

api = UserDto.api
userinfo_schema = UserInfoSchema()
userinfos_schema = UserInfoSchema(many=True)

contact_model = api.model('Contact', {
    'id': fields.Integer(description='Contact ID', example=1),
    'phone': fields.String(description='Phone number', example='+1234567890'),
    'address': fields.String(description='Address', example='123 Main Street'),
    'city': fields.String(description='City', example='New York'),
    'country': fields.String(description='Country', example='USA')
})

role_model = api.model('Role', {
    'id': fields.Integer(description='Role ID', example=1),
    'name': fields.String(description='Role name', example=RoleType.ADMIN.value)
})

user_details_model = api.model('UserDetails', {
    'id': fields.Integer(description='User ID', example=1),
    'username': fields.String(description='Username', example='john_doe'),
    'first_name': fields.String(description='First name', example='John'),
    'last_name': fields.String(description='Last name', example='Doe'),
    'active': fields.Boolean(description='Active status', example=True),
    'company': fields.String(description='Company', example='Example Company'),
    'sex': fields.String(description='Gender', example='M'),
    'contact': fields.Nested(contact_model, description='User contact information'),
    'role': fields.Nested(role_model, description='User role information'),
    'email': fields.String(description='Email address', example='john@example.com')
})


@api.route("/")
class UserInfoListController(Resource):

    @token_auth.login_required
    @api.doc('Get list of users')
    @api.doc(responses={200: 'OK', 404: 'User not found'}, security='Bearer Auth', model=[user_details_model])
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
    @api.doc(responses={200: 'OK', 404: 'User not found'}, security='Bearer Auth', model=user_details_model)
    def get(self, id):
        """Get a user by id"""
        user = UserInfo.query.get(id)

        if not user:
            return {'message': 'User not found'}, 404

        return userinfo_schema.dump(user), 200
