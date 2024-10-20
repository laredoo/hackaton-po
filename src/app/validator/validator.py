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

        return self.error, self.use_cases

    def check_has_schedule(self):
        use_case: dict = self.get_use_case()

        dispon_profissional: pd.DataFrame = use_case["DisponProfissional"]

        dispon_profissional["profissional"].ffill()

        result = dispon_profissional.groupby("profissional").apply(
            self.check_schedule, include_groups=False
        )

        for profissional, tem_horario in result.items():
            if not tem_horario:
                message = f"O profissional {profissional} NÃO tem horários alocados."
                error_dict: dict = self.write_inconsistency(
                    tabela="DisponProfissional", tipo="ERRO", mensagem=message
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
