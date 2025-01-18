from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from app.config import Config
from app.models.user import User
from app.services.personality_analyzer_service import PersonalityAnalyzerService
from app.constants.questionnaire import PERSONALITY_QUESTIONS

class ChatService:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, api_key=Config.OPENAI_API_KEY)
        self.personality_prompt = ChatPromptTemplate.from_messages([
            ("system", """Given the message: {message}

keeping in mind their communication style and preferences.
The response should feel natural and personal, reflecting their way of talking."""),
            MessagesPlaceholder(variable_name="message"),
        ])
        
        self.chat_chain = LLMChain(prompt=self.personality_prompt, llm=self.llm)
        self.personality_analyzer = PersonalityAnalyzerService()

    def analyze_and_store_personality(self, user_id):
        """Analyze user's questionnaire responses and store personality profile"""
        user = User.get_user(user_id)
        if not user:
            raise ValueError("User not found")

        
        answers = user.get('questionnaire_responses', {})


        if not answers:
            raise ValueError("No questionnaire responses found")

        
        try:
            personality_profile = self.personality_analyzer.analyze_personality(
                PERSONALITY_QUESTIONS, 
                answers
            )
            
            
            User.update_personality_profile(user_id, personality_profile)
            
            return personality_profile
        except Exception as e:
            raise ValueError(f"Failed to analyze personality: {str(e)}")

    def get_user_info(self, user_id):
        user = User.get_user(user_id)
        if not user:
            raise ValueError("User not found")
            
        
        personality_profile = user.get('personality_profile')
        if not personality_profile:
            personality_profile = self.analyze_and_store_personality(user_id)

        personal_info = user.get('personal_info', {})
        
        return {
            "name": personal_info.get('name', 'Unknown'),
            "age": personal_info.get('age', 'Unknown'),
            "gender": personal_info.get('gender', 'Unknown'),
            "location": personal_info.get('location', 'Unknown'),
            "intro_style": personality_profile.get('intro_style', ''),
            "preferred_people": personality_profile.get('preferred_people', ''),
            "conversation_style": personality_profile.get('conversation_style', ''),
            "compliment_response": personality_profile.get('compliment_response', '')
        }

    def chat(self, input_message, user_id):
        user_info = self.get_user_info(user_id)
        chat_history = User.get_chat_history(user_id)
        messages = []
        system_message = SystemMessage(content=f"""
You are acting as {user_info['name']}, a {user_info['age']} year old {user_info['gender']} from {user_info['location']}. 
Based on their communication style:
- They introduce themselves like: "{user_info['intro_style']}"
- They prefer talking to: "{user_info['preferred_people']}"
- Their conversation style is: "{user_info['conversation_style']}"
- They respond to compliments by: "{user_info['compliment_response']}"

Maintain this personality and communication style while responding to messages.
""")
        messages.append(system_message)

        # Add chat history
        for msg in chat_history['messages']:
            if msg['sender'] == 'user':
                messages.append(HumanMessage(content=msg['message']))
            elif msg['sender'] == 'ai':
                messages.append(AIMessage(content=msg['message']))

        # Add new message
        messages.append(HumanMessage(content=input_message))

        # Generate response
        response = self.chat_chain.predict(message=messages)

        # Update chat history
        chat_history['messages'].append({"sender": "user", "message": input_message})
        chat_history['messages'].append({"sender": "ai", "message": response})

        User.update_chat_history(user_id, chat_history['messages'])

        return response

    
