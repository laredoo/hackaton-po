from src.app.validator.controller import ValidatorController
from src.app.repository.input_import.controller import ModelImportController


class Factory:

    def get_validator_repository(self):
        return ValidatorController(name="validator")

    def get_model_import_repository(self):
        return ModelImportController()
