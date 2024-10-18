from flask import Blueprint
from flask_restx import Api
from flask_jwt_extended import JWTManager

api_bp = Blueprint('api', __name__)
authorizations = {
    'jwt': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token"
    }
}

api = Api(api_bp, version='1.0', title='Todo API',
          description='A simple Todo API',
          authorizations=authorizations,
          security='jwt')

from . import auth, todos