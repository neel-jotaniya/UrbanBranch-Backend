from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from app.routes.chat import ChatResource
from app.routes.user import UserHistoryResource, UsersResource
from app.routes.onboarding import OnboardingResource


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

    api = Api(app)
    
    api.add_resource(UsersResource, '/users')
    api.add_resource(UserHistoryResource, '/users/<string:user_id>') 
    api.add_resource(ChatResource, '/chat')
    api.add_resource(OnboardingResource, '/onboarding')

    return app 

