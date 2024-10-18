from flask_restx import Resource, Namespace
from flask import request
from flask_jwt_extended import create_access_token
from app.services.user_service import UserService
from app.schemas.user_schema import user_schema

auth_ns = Namespace('auth', description='Authentication operations')

@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.expect(user_schema)
    def post(self):
        data = request.json
        user, error = UserService.register_user(data['username'], data['email'], data['password'])
        if error:
            return {'message': error}, 400
        return user_schema.dump(user), 201

@auth_ns.route('/login')
class Login(Resource):
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