from src.app.validator.controller import ValidatorController


class Factory:

    def get_validator_repository(self):
        return ValidatorController(name="validator")
