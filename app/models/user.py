from datetime import datetime
from pymongo import MongoClient
from app.config import Config
from bson import ObjectId

client = MongoClient(Config.MONGODB_URI)
db = client['UM_AI']

class User:
    collection = db['UM_AI_Users']
    chat_history_collection = db['chat_history_db']

    @staticmethod
    def create_user(user_data, questionnaire_responses):
        user = {
            "personal_info": user_data,
            "questionnaire_responses": questionnaire_responses,
            "created_at": datetime.utcnow()
        }
        return User.collection.insert_one(user)

    @staticmethod
    def get_user(user_id):
        return User.collection.find_one({"_id": ObjectId(user_id)})

    @staticmethod
    def get_chat_history(user_id):
        """Retrieve chat history for a user"""
        return User.chat_history_collection.find_one({"user_id": user_id}) or {"user_id": user_id, "messages": []}

    @staticmethod
    def update_chat_history(user_id, messages):
        """Update chat history for a user"""
        User.chat_history_collection.update_one(
            {"user_id": user_id},
            {"$set": {"messages": messages}},
            upsert=True
        )
        print(User.get_chat_history(user_id))

    @staticmethod
    def update_personality_profile(user_id: str, profile: dict):
        """Update user's personality profile in the database"""
        User.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"personality_profile": profile}}
        )

    @staticmethod
    def get_all_users():
        """Retrieve all users from the database with only name and ID"""
        users = list(User.collection.find({}, {"personal_info.name": 1}))  
        simplified_users = []
        for user in users:
            simplified_users.append({
                "id": str(user['_id']),
                "name": user['personal_info'].get('name', 'Unknown')
            })
        print(simplified_users)
        return simplified_users

    @staticmethod
    def get_user_with_history(user_id):
        """Retrieve user data along with their chat history"""
        user_data = User.get_user(user_id)
        if not user_data:
            raise ValueError("User not found")
        user_data['_id'] = str(user_data['_id'])
        if 'created_at' in user_data:
            user_data['created_at'] = user_data['created_at'].isoformat()
        chat_history = User.get_chat_history(user_id)
        if '_id' in chat_history:
            chat_history['_id'] = str(chat_history['_id'])
        user_data['chat_history'] = chat_history
        print("-------------------", user_data)
        return user_data
      