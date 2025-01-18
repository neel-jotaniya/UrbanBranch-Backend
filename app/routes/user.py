from flask_restful import Resource
from flask import request
from app.models.user import User

            
class UsersResource(Resource):
    def get(self):
        try:
            users = User.get_all_users()
            print(users)
            return {'users': users}, 200
        except Exception as e:
            return {'error': 'An unexpected error occurred'}, 500

class UserHistoryResource(Resource):
    def get(self, user_id):
        try:
            user_info = User.get_user_with_history(user_id)
            return {'user_info': user_info}, 200
        except ValueError as e:
            return {'error': str(e)}, 404
        except Exception as e:
            return {'error': 'An unexpected error occurred'}, 500

