from datetime import datetime
import pandas as pd


class BaseValidator:
    def __init__(self, path: str):
        self.path = path
        self.error_type = "ERRO"
        self.warning_type = "AVISO"

    def get_use_case(self) -> dict:
        return pd.read_excel(self.path, sheet_name=None)

    def check_schedule(self, group):
        if (group.iloc[:, 2:] == "X").any().any():
            return True
        else:
            return False

    def write_inconsistency(self, tabela: str, tipo: str, mensagem: str):

        data_atualização: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        errors_data: dict = {
            "tabela": [tabela],
            "tipo": [tipo],
            "mensagem": [mensagem],
            "data_atualização": [data_atualização],
        }

        return errors_data
