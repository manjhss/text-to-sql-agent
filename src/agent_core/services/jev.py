from typesafe_sdk import Choice, Noul, Score, TypeSafeClient

from src.config.settings import settings


class JEVService:
    """manages llm operations"""

    def __init__(self):
        self.api_key = settings.jev_api_key
        self.client = TypeSafeClient()


jev_service = JEVService()
