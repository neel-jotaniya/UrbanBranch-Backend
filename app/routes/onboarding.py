from flask_restful import Resource, Api, reqparse
from flask import request
from app.models.user import User

class OnboardingResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('personal_info', type=dict, required=True, help='Personal information is required and must be a dictionary.')
        


    def post(self):
        data = request.json  
        personal_info = data.get('personal_info')
        questionnaire_responses = data.get('questionnaire_responses')
        
        required_personal_fields = ['name', 'age', 'sex', 'location', 'education', 'job_title', 'company_name']
        if not all(field in personal_info for field in required_personal_fields):
            return {'error': 'Missing required personal information'}, 400
        
        if len(questionnaire_responses) != 15:
            return {'error': 'Invalid questionnaire responses'}, 400

        try:
            user_id = User.create_user(personal_info, questionnaire_responses)
            return {'user_id': str(user_id.inserted_id)}, 201
        except Exception as e:
            return {'error': str(e)}, 500
