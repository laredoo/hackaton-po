from src.app.problem_instance.controller import ProblemInstanceController
from src.app.validator.controller import ValidatorController
from src.app.repository.input_import.controller import ModelImportController
from src.app.validator.validator import Validator


class Factory:

    def get_input_validator_handler(self, path: str):
        return Validator(path)

    def get_validator_controller(self, path: str):
        return ValidatorController(validator=self.get_input_validator_handler(path))

    def get_model_import_controller(self):
        return ModelImportController()

    def problem_instance_controller(
        self,
        local_list,
        zbr,
        patients_disponibility,
        professional_disponibility,
        professional_hours,
    ):
        return ProblemInstanceController(
            local_list,
            zbr,
            patients_disponibility,
            professional_disponibility,
            professional_hours,
        )
