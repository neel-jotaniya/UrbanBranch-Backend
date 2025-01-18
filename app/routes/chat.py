from flask_restful import Resource, Api, reqparse
from flask import request

from app.services.chat_service import ChatService

chat_service = ChatService()

class ChatResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('user_id', type=str, required=True)
        self.parser.add_argument('message', type=str, required=True)

    def post(self):
        data = request.json  # Parse the JSON payload
        user_id = data.get('user_id')
        message = data.get('message')
        try:
            response = chat_service.chat(message, user_id)
            return {'response': response}, 200
        except ValueError as e:
            return {'error': str(e)}, 404
        except Exception as e:
            return {'error': 'An unexpected error occurred'}, 500

