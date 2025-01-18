from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    MONGODB_URI = os.getenv('MONGODB_URI')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    MODEL_NAME = "gpt-3.5-turbo"  