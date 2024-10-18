from flask import Blueprint
from flask_restx import Api

api_bp = Blueprint('api', __name__)
api = Api(api_bp, version='1.0', title='Todo API',
          description='A simple Todo API')

from . import auth, todos