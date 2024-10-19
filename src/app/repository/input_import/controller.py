import pandas as pd

from src.core.config import config


class ModelImportController:
    def __init__(self):
        self.name = "ModelImportController"

    def format_disponibility(self, row: pd.Series) -> list:
        disponibilidade = []

        for hora in range(8, 21):
            hr_col = f"hr_{hora}"
            if row[hr_col] == "X":
                disponibilidade.append(f"{hora}")

        return disponibilidade

    def local_disponibility(self, row: pd.Series, projects: list) -> list:
        locais = [project for project in projects if row[project] == "X"]

        """
        if row['virtual_epsi'] == 'X':
            locais.append('VIRTUAL')
        """

        return locais

    def virtual_disponibility(self, row: pd.Series) -> bool:
        if row["virtual_epsi"] == "X":
            return True
        return False

    def check_age(self, row: pd.Series) -> str:
        if row["idade"] < 12:
            return "infantil"
        elif 12 >= row["idade"] < 18:
            return "adolescente"
        return "adulto"

    def read_xlsx(self, path) -> pd.DataFrame:
        return pd.read_excel(path, sheet_name=None)

    def index_patients_ages(self, use_case: pd.DataFrame) -> pd.DataFrame:
        use_case["IdadePaciente"]["age_range"] = use_case["IdadePaciente"].apply(
            self.check_age, axis=1
        )

        return use_case

    def aggregate_patients_table(self, use_case: pd.DataFrame) -> pd.DataFrame:
        aggregated_patients_table = pd.merge(
            use_case["DisponPaciente"].ffill(),
            use_case["LocalPaciente"].ffill(),
            on=["paciente", "dia_semana"],
            how="inner",
        )

        return aggregated_patients_table

    def format_patients_consolidated_table(
        self, consolidated_table: pd.DataFrame
    ) -> pd.DataFrame:
        projects = config.PROJECTS
        consolidated_table["hours"] = consolidated_table.apply(
            self.format_disponibility, axis=1
        )
        consolidated_table["available_places"] = consolidated_table.apply(
            lambda x: self.local_disponibility(x, projects), axis=1
        )
        consolidated_table["virtual"] = consolidated_table.apply(
            self.virtual_disponibility, axis=1
        )

        return consolidated_table

    def consolidate_table(self, use_case: pd.DataFrame) -> pd.DataFrame:
        consolidated_table: pd.DataFrame = pd.DataFrame()

        use_case: pd.DataFrame = self.index_patients_ages(use_case)

        aggregated_patients_table: pd.DataFrame = self.aggregate_patients_table(
            use_case
        )

        pre_consolidated_table: pd.DataFrame = pd.merge(
            aggregated_patients_table,
            use_case["IdadePaciente"],
            on="paciente",
            how="inner",
        )

        consolidated_table: pd.DataFrame = self.format_patients_consolidated_table(
            pre_consolidated_table
        )

        return consolidated_table

    def handle_input(self, path) -> pd.DataFrame:

        use_case: pd.DataFrame = self.read_xlsx(path)

        consolidated_table: pd.DataFrame = self.consolidate_table(use_case=use_case)

        return consolidated_table
