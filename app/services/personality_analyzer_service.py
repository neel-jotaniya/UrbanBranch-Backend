from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from app.config import Config

class PersonalityAnalyzerService:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3, api_key=Config.OPENAI_API_KEY)
        self.analyzer_prompt = PromptTemplate(
            input_variables=["qa_pairs"],
            template="""Based on the following questionnaire responses, analyze the person's communication style and create a personality profile.

{qa_pairs}

Generate a JSON response with the following fields:
- intro_style: A natural sentence describing how they would typically introduce themselves
- preferred_people: Description of the types of people they prefer interacting with
- conversation_style: Description of their communication style and tone
- compliment_response: How they typically respond to compliments

Values for these fields should not be more than 10 words.
Format the response as a valid JSON object."""
        )
        
        self.analyzer_chain = LLMChain(prompt=self.analyzer_prompt, llm=self.llm)

    def analyze_personality(self, questions: list[str], answers: list[str]) -> dict:
        """
        Analyzes user's questionnaire responses to generate a personality profile.
        
        Args:
            questions (list[str]): List of questionnaire questions
            answers (list[str]): List of user's answers corresponding to the questions
            
        Returns:
            dict: Personality profile containing intro_style, preferred_people,
                 conversation_style, and compliment_response
        """
        # Format Q&A pairs
        qa_pairs = "\n".join([f"Q{i+1}: {q}\nA{i+1}: {a}" for i, (q, a) in enumerate(zip(questions, answers))])
        
        # Generate personality profile
        result = self.analyzer_chain.predict(qa_pairs=qa_pairs)
        
        # Parse and return the JSON response
        try:
            import json
            return json.loads(result)
        except json.JSONDecodeError:
            raise ValueError("Failed to generate valid personality profile") 
        



