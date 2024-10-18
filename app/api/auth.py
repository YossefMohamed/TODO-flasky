from flask_restx import Resource, Namespace, fields
from flask import request
from flask_jwt_extended import create_access_token
from app.services.user_service import UserService
from app.schemas.user_schema import user_schema

auth_ns = Namespace('auth', description='Authentication operations')

# Define models for Swagger UI
user_model = auth_ns.model('User', {
    'username': fields.String(required=True, description='User username'),
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

login_model = auth_ns.model('Login', {
    'username': fields.String(required=True, description='User username'),
    'password': fields.String(required=True, description='User password')
})

@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.expect(user_model)
    @auth_ns.doc(responses={201: 'Success', 400: 'Validation Error'})
    def post(self):
        data = request.json
        user, error = UserService.register_user(data['username'], data['email'], data['password'])
        if error:
            return {'message': error}, 400
        return user_schema.dump(user), 201

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    @auth_ns.doc(responses={200: 'Success', 401: 'Unauthorized'})
    def post(self):
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        user = UserService.authenticate_user(username, password)
        if not user:
            return {'message': 'Invalid credentials'}, 401
        access_token = create_access_token(identity=username)
        return {'access_token': access_token}, 200

from app.api import api
api.add_namespace(auth_ns)