from typesafe_sdk import TypeSafeClient

from src.config.settings import settings


class JEVService:
    """manages llm operations"""

    def __init__(self):
        self.api_key = settings.jev_api_key
        self.client = TypeSafeClient(api_key=self.api_key)


jev_service = JEVService()
