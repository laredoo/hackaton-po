import pandas as pd


class BaseValidator:
    def __init__(self, path: str):
        self.path = path
        self.error_type = "ERRO"
        self.warning_type = "AVISO"

    def get_use_case(self) -> dict:
        return pd.read_excel(self.path, sheet_name=None)
