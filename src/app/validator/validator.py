import pandas as pd
from src.app.validator.base_validator import BaseValidator


class Validator(BaseValidator):
    def __init__(self, path: str):
        super().__init__(path)
        self.error: bool = False

    def check_patient_age(self):
        use_case: dict = self.get_use_case()

        idade_paciente: pd.DataFrame = use_case["IdadePaciente"]

        missing_age = idade_paciente[idade_paciente["idade"].isnull()]

        if missing_age["idade"].isnull().any():
            message: str = (
                f"Paciente [{missing_age['paciente'].iloc[0]}] sem idade cadastrada"
            )

        self.error: bool = True

        return message, self.error
