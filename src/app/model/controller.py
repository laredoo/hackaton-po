from src.core.factory.factory import Factory
from core.config import config


class ValidatorController:
    def __init__(self, name: str):
        self.name = name
        self.language = config.DEFAULT_LANGUAGE

    def return_language(self):
        return self.language
