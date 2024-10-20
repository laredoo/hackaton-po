from datetime import datetime
import pandas as pd


class BaseValidator:
    def __init__(self, path: str):
        self.path = path
        self.error_type = "ERRO"
        self.warning_type = "AVISO"

    def get_use_case(self) -> dict:
        return pd.read_excel(self.path, sheet_name=None)

    def validate_x_professional_local(self, row):
        return any(str(cell).lower() == "x" for cell in row[1:] if pd.notna(cell))

    def validate_x_patient_local(self, row):
        return any(str(cell).lower() == "x" for cell in row[2:] if pd.notna(cell))

    def check_schedule(self, group, professional: bool = False):
        if professional:
            if (group.iloc[:, 0:] == "X").any().any():
                print((group.iloc[:, 0:] == "X").any().any())
                return True
            elif (group.iloc[:, 0:] == "x").any().any():
                return True
            else:
                return False
        else:
            if (group.iloc[:, 1:] == "X").any().any():
                return True
            elif (group.iloc[:, 1:] == "x").any().any():
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
