from datetime import datetime
import pandas as pd
from src.app.validator.base_validator import BaseValidator


class Validator(BaseValidator):
    def __init__(self, path: str, use_cases: dict):
        super().__init__(path)
        self.use_cases: dict = use_cases

    def check_patient_age(self) -> bool:

        error: bool = False

        error_list: list = []

        idade_paciente: pd.DataFrame = self.use_cases["IdadePaciente"]

        missing_age = idade_paciente[idade_paciente["idade"].isnull()]

        if missing_age["idade"].isnull().any():
            for _, l in missing_age.iterrows():
                message: str = f"Paciente {l['paciente']} sem idade cadastrada"
                error_dict: dict = {
                    "tabela": "IdadePaciente",
                    "tipo": "ERRO",
                    "mensagem": message,
                    "data_atualização": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
                error_list.append(error_dict)

        if error_list:
            df_erro = pd.DataFrame(error_list)
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
                error: bool = True

        return error

    def check_professional_availability(self) -> bool:

        error: bool = False
        error_list = []

        regra_profissional: pd.DataFrame = self.use_cases["RegraProfissional"]

        missing_hours = regra_profissional[regra_profissional["horas_semana"].isnull()]

        if regra_profissional["horas_semana"].isnull().any():
            for _, l in missing_hours.iterrows():
                message: str = (
                    f"Profissional {l['profissional']} sem HORÁRIO cadastrado. Não será alocado"
                )
                error_dict: dict = {
                    "tabela": "RegraProfissional",
                    "tipo": "AVISO",
                    "mensagem": message,
                    "data_atualização": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
                error_list.append(error_dict)

        if error_list:
            df_erro = pd.DataFrame(error_list)
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
                error: bool = True

        return error

    def _get_missing_type(
        self, regra_profissional: pd.DataFrame, error_list: tuple[list, bool]
    ) -> list:
        error: bool = False

        missing_type = regra_profissional[regra_profissional["tipo"].isnull()]

        if missing_type["tipo"].isnull().any():
            for _, l in missing_type.iterrows():
                message: str = f"Paciente {l['profissional']} sem tipo cadastrado"

                error_dict: dict = {
                    "tabela": "RegraProfissional",
                    "tipo": "AVISO",
                    "mensagem": message,
                    "data_atualização": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }

                error: bool = True

                error_list.append(error_dict)
        return error_list, error

    def _get_invalid_type(
        self, regra_profissional: pd.DataFrame, error_list: tuple[list, bool]
    ) -> list:
        error: bool = False

        valores_invalidos = regra_profissional[
            ~regra_profissional["tipo"].isin(["V", "E", "v", "e"])
        ]

        valores_invalidos = valores_invalidos.dropna(subset=["tipo"])

        if not valores_invalidos.empty:
            for _, l in valores_invalidos.iterrows():
                message: str = (
                    f"Paciente {l['profissional']} tem tipo cadastrado inválido: {l['tipo']}"
                )

                error_dict: dict = {
                    "tabela": "RegraProfissional",
                    "tipo": "AVISO",
                    "mensagem": message,
                    "data_atualização": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }

                error_list.append(error_dict)

            error: bool = True

        return error_list, error

    def check_professional_type(self) -> bool:

        error_missing_type: bool = False
        error_invalid_type: bool = False
        error_list = []

        regra_profissional: pd.DataFrame = self.use_cases["RegraProfissional"]

        error_list, error_missing_type = self._get_missing_type(
            regra_profissional, error_list
        )

        error_list, error_invalid_type = self._get_invalid_type(
            regra_profissional, error_list
        )

        df_erro = pd.DataFrame(error_list)

        if error_list:
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

        return error_missing_type or error_invalid_type

    def check_has_schedule_profissional(self) -> bool:

        error: bool = False

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
                    "tipo": "AVISO",
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
            error: bool = True

        return error

    def check_professional_has_age_range(self) -> bool:
        error: bool = False

        regra_profissional: pd.DataFrame = self.use_cases["RegraProfissional"]

        regra_profissional["valido"] = regra_profissional.apply(
            self.validade_x_professional_age_range, axis=1
        )

        grouped = regra_profissional.groupby("profissional")["valido"].apply(
            lambda x: (x == False).all()
        )

        dict_list = []

        for profissional, valido in grouped.items():
            if valido:
                error_dict = {
                    "tabela": "RegraProfissional",
                    "tipo": "AVISO",
                    "mensagem": f"O profissional {profissional} NÃO tem NENHUMA idade de preferência alocado. Ele não será alocado.",
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
            error: bool = True

        return error

    def check_has_places_profissional(self):

        error: bool = False

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
            error: bool = True

        return error

    def check_has_schedule_patient(self):

        error: bool = False

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
                    "tipo": "AVISO",
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
            error: bool = True

        return error

    def check_has_places_patient(self):

        error: bool = False

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
            error: bool = True

        return error

    def check_same_professionals(self):

        error: bool = False

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
            error: bool = True

        return error

    def check_same_patients(self):

        error: bool = False

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
            error: bool = True

        return error
