from datetime import datetime
import pandas as pd
from src.app.validator.base_validator import BaseValidator


class Validator(BaseValidator):
    def __init__(self, path: str, use_cases: dict):
        super().__init__(path)
        self.error: bool = False
        self.use_cases: dict = use_cases

    def check_patient_age(self):

        idade_paciente: pd.DataFrame = self.use_cases["IdadePaciente"]

        missing_age = idade_paciente[idade_paciente["idade"].isnull()]

        if missing_age["idade"].isnull().any():
            message: str = (
                f"Paciente [{missing_age['paciente'].iloc[0]}] sem idade cadastrada"
            )
            error_dict: dict = self.write_inconsistency(
                tabela="IdadePaciente", tipo="ERRO", mensagem=message
            )
            df_erro = pd.DataFrame(error_dict)
            with pd.ExcelWriter(
                self.path, engine="openpyxl", mode="a", if_sheet_exists="overlay"
            ) as writer:
                df_erro.to_excel(
                    writer,
                    sheet_name="Inconsistência",
                    index=False,
                    header=False,
                    startrow=writer.sheets["Inconsistência"].max_row,
                )

            self.error: bool = True

        return self.error

    def check_has_schedule_profissional(self):

        dispon_profissional: pd.DataFrame = self.use_cases["DisponProfissional"]

        dispon_profissional["profissional"] = dispon_profissional[
            "profissional"
        ].ffill()

        dispon_profissional["valido"] = dispon_profissional.apply(
            self.validate_x_professional_local, axis=1
        )

        grouped = dispon_profissional.groupby("profissional")["valido"].apply(
            lambda x: (x == False).all()
        )

        dict_list = []

        for profissional, valido in grouped.items():
            if valido:
                error_dict = {
                    "tabela": "DisponProfissional",
                    "tipo": "ERRO",
                    "mensagem": f"O profissional {profissional} NÃO tem horários alocados.",
                    "data_atualização": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
                dict_list.append(error_dict)

        if dict_list:
            df_erro = pd.DataFrame(dict_list)
            with pd.ExcelWriter(
                self.path, engine="openpyxl", mode="a", if_sheet_exists="overlay"
            ) as writer:
                df_erro.to_excel(
                    writer,
                    sheet_name="Inconsistência",
                    index=False,
                    header=False,
                    startrow=writer.sheets["Inconsistência"].max_row,
                )
            self.error: bool = True

        return self.error

    def check_has_places_profissional(self):
        local_profissional: pd.DataFrame = self.use_cases["LocalProfissional"]

        local_profissional["valido"] = local_profissional.apply(
            self.validate_x_professional_local, axis=1
        )

        grouped = local_profissional.groupby("profissional")["valido"].apply(
            lambda x: (x == False).all()
        )

        dict_list = []

        for profissional, valido in grouped.items():
            if valido:
                error_dict = {
                    "tabela": "LocalProfissional",
                    "tipo": "ERRO",
                    "mensagem": f"O profissional {profissional} NÃO tem lugares alocados.",
                    "data_atualização": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
                dict_list.append(error_dict)

        if dict_list:
            df_erro = pd.DataFrame(dict_list)
            with pd.ExcelWriter(
                self.path, engine="openpyxl", mode="a", if_sheet_exists="overlay"
            ) as writer:
                df_erro.to_excel(
                    writer,
                    sheet_name="Inconsistência",
                    index=False,
                    header=False,
                    startrow=writer.sheets["Inconsistência"].max_row,
                )
            self.error: bool = True

        return self.error

    def check_has_schedule_patient(self):

        dispon_paciente: pd.DataFrame = self.use_cases["DisponPaciente"]

        dispon_paciente["paciente"] = dispon_paciente["paciente"].ffill()

        dispon_paciente["valido"] = dispon_paciente.apply(
            self.validate_x_professional_local, axis=1
        )

        grouped = dispon_paciente.groupby("paciente")["valido"].apply(
            lambda x: (x == False).all()
        )

        dict_list = []

        for paciente, valido in grouped.items():
            if valido:
                error_dict = {
                    "tabela": "DisponPaciente",
                    "tipo": "ERRO",
                    "mensagem": f"O paciente {paciente} NÃO tem horários alocados.",
                    "data_atualização": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
                dict_list.append(error_dict)

        if dict_list:
            df_erro = pd.DataFrame(dict_list)
            with pd.ExcelWriter(
                self.path, engine="openpyxl", mode="a", if_sheet_exists="overlay"
            ) as writer:
                df_erro.to_excel(
                    writer,
                    sheet_name="Inconsistência",
                    index=False,
                    header=False,
                    startrow=writer.sheets["Inconsistência"].max_row,
                )
            self.error: bool = True

        return self.error

    def check_has_places_patient(self):
        local_paciente: pd.DataFrame = self.use_cases["LocalPaciente"]

        local_paciente["paciente"] = local_paciente["paciente"].ffill()

        local_paciente["valido"] = local_paciente.apply(
            self.validate_x_patient_local, axis=1
        )

        grouped = local_paciente.groupby("paciente")["valido"].apply(
            lambda x: (x == False).all()
        )

        dict_list = []

        for paciente, valido in grouped.items():
            if valido:
                # print(paciente, valido)
                error_dict = {
                    "tabela": "LocalPaciente",
                    "tipo": "ERRO",
                    "mensagem": f"O paciente {paciente} NÃO tem lugares alocados.",
                    "data_atualização": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
                dict_list.append(error_dict)

        if dict_list:
            df_erro = pd.DataFrame(dict_list)
            with pd.ExcelWriter(
                self.path, engine="openpyxl", mode="a", if_sheet_exists="overlay"
            ) as writer:
                df_erro.to_excel(
                    writer,
                    sheet_name="Inconsistência",
                    index=False,
                    header=False,
                    startrow=writer.sheets["Inconsistência"].max_row,
                )
            self.error: bool = True

        return self.error

    def check_same_professionals(self):
        regra_profissional: pd.DataFrame = self.use_cases["RegraProfissional"]
        dispon_profissional: pd.DataFrame = self.use_cases["DisponProfissional"]
        local_profissional: pd.DataFrame = self.use_cases["LocalProfissional"]

        col = "profissional"

        dict_list = []

        con1 = (
            regra_profissional[col].dropna().unique()
            == dispon_profissional[col].dropna().unique()
        ).all()

        con2 = (
            dispon_profissional[col].dropna().unique()
            == local_profissional[col].dropna().unique()
        ).all()

        if not (con1 and con2):
            if con1:
                tabela = "LocalProfissional"
            elif con2:
                tabela = "RegraProfissional"
            else:
                tabela = "DisponibilidadeProfissional"

            error_dict = {
                "tabela": tabela,
                "tipo": "ERRO",
                "mensagem": f"As listas de profissional estão diferentes.",
                "data_atualização": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            dict_list.append(error_dict)

        if dict_list:
            df_erro = pd.DataFrame(dict_list)
            with pd.ExcelWriter(
                self.path, engine="openpyxl", mode="a", if_sheet_exists="overlay"
            ) as writer:
                df_erro.to_excel(
                    writer,
                    sheet_name="Inconsistência",
                    index=False,
                    header=False,
                    startrow=writer.sheets["Inconsistência"].max_row,
                )
            self.error: bool = True

        return self.error

    def check_same_patients(self):
        idade_paciente: pd.DataFrame = self.use_cases["IdadePaciente"]
        dispon_paciente: pd.DataFrame = self.use_cases["DisponPaciente"]
        local_paciente: pd.DataFrame = self.use_cases["LocalPaciente"]

        col = "paciente"

        dict_list = []

        con1 = (
            idade_paciente[col].dropna().unique()
            == dispon_paciente[col].dropna().unique()
        ).all()

        con2 = (
            dispon_paciente[col].dropna().unique()
            == local_paciente[col].dropna().unique()
        ).all()

        if not (con1 and con2):
            if con1:
                tabela = "LocalProfissional"
            elif con2:
                tabela = "IdadePaciente"
            else:
                tabela = "DisponibilidadePaciente"

            error_dict = {
                "tabela": tabela,
                "tipo": "ERRO",
                "mensagem": f"As listas de paciente estão diferentes.",
                "data_atualização": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            dict_list.append(error_dict)

        if dict_list:
            df_erro = pd.DataFrame(dict_list)
            with pd.ExcelWriter(
                self.path, engine="openpyxl", mode="a", if_sheet_exists="overlay"
            ) as writer:
                df_erro.to_excel(
                    writer,
                    sheet_name="Inconsistência",
                    index=False,
                    header=False,
                    startrow=writer.sheets["Inconsistência"].max_row,
                )
            self.error: bool = True

        return self.error
