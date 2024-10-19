from src.app.problem_instance.controller import ProblemInstanceController
from src.app.validator.controller import ValidatorController
from src.app.repository.input_import.controller import ModelImportController


class Factory:

    def get_validator_repository(self):
        return ValidatorController(name="validator")

    def get_model_import_controller(self):
        return ModelImportController()

    def problem_instance_controller(
        self, zbr, patients_disponibility, professional_disponibility
    ):
        return ProblemInstanceController(
            zbr, patients_disponibility, professional_disponibility
        )
