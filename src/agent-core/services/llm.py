from langchain_groq import ChatGroq

from src.config.settings import settings


class LLMService:
    """manages llm operations"""

    def __init__(self, temperature: int = 1):
        self.model = settings.groq_model
        self.temperature = temperature
        self.api_key = settings.groq_api_key

        self.llm = ChatGroq(
            model=self.model, temperature=self.temperature, api_key=self.api_key
        )