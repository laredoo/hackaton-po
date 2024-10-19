import logging
from typing import Tuple
import pandas as pd

from src.core.config import config

logger = logging.getLogger(__name__)


class ModelImportController:
    def __init__(self):
        self.name = "ModelImportController"

    def format_disponibility(self, row: pd.Series) -> list:
        disponibilidade = []

        for hora in range(8, 21):
            hr_col = f"hr_{hora}"
            if row[hr_col] == "X" or row[hr_col] == "x":
                disponibilidade.append(f"{hora}")

        return disponibilidade

    def local_disponibility(self, row: pd.Series, projects: list) -> list:
        locais = [
            project
            for project in projects
            if row[project] == "X" or row[project] == "x"
        ]

        if row["virtual_epsi"] == "X" or row["virtual_epsi"] == "x":
            locais.append("VIRTUAL")

        return locais

    def virtual_disponibility(self, row: pd.Series) -> bool:
        if row["virtual_epsi"] == "X" or row["virtual_epsi"] == "x":
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
        # logger.info("[BACKEND] Getting patients age range")

        use_case["IdadePaciente"]["patient_age_range"] = use_case[
            "IdadePaciente"
        ].apply(self.check_age, axis=1)

        return use_case

    def aggregate_patients_table(self, use_case: pd.DataFrame) -> pd.DataFrame:
        # logger.info("[BACKEND] Merging DisponPaciente and LocalPaciente")

        # filling paciene column
        use_case["DisponPaciente"]["paciente"] = use_case["DisponPaciente"][
            "paciente"
        ].ffill()
        use_case["LocalPaciente"]["paciente"] = use_case["LocalPaciente"][
            "paciente"
        ].ffill()

        aggregated_patients_table = pd.merge(
            use_case["DisponPaciente"],
            use_case["LocalPaciente"],
            on=["paciente", "dia_semana"],
            how="inner",
        )

        return aggregated_patients_table

    def format_patients_consolidated_table(
        self, consolidated_table: pd.DataFrame
    ) -> pd.DataFrame:
        # logger.info("[BACKEND] Applying patients rules")

        projects = config.PROJECTS
        consolidated_table["patient_hours"] = consolidated_table.apply(
            self.format_disponibility, axis=1
        )
        consolidated_table["patient_available_places"] = consolidated_table.apply(
            lambda x: self.local_disponibility(x, projects), axis=1
        )

        # consolidated_table["virtual"] = consolidated_table.apply(
        #     self.virtual_disponibility, axis=1
        # )

        return consolidated_table

    def consolidate_patients_table(
        self, path: str
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        logger.info("[BACKEND] Reading PATIENTS DATA")
        use_case: pd.DataFrame = self.read_xlsx(path)

        patients_consolidated_table = pd.DataFrame()

        use_case: pd.DataFrame = self.index_patients_ages(use_case)

        aggregated_patients_table: pd.DataFrame = self.aggregate_patients_table(
            use_case
        )

        # logger.info("[BACKEND] Merging aggregated_patients_table and IdadePaciente")
        pre_consolidated_table: pd.DataFrame = pd.merge(
            aggregated_patients_table,
            use_case["IdadePaciente"],
            on="paciente",
            how="inner",
        )

        patients: pd.DataFrame = self.format_patients_consolidated_table(
            pre_consolidated_table
        )

        # logger.info("[BACKEND] Returning consolidated patients table")
        patients_consolidated_table = patients.loc[
            :,
            [
                "paciente",
                "dia_semana",
                "patient_hours",
                "patient_available_places",
                "patient_age_range",
            ],
        ]

        return patients, patients_consolidated_table

    def age_range_disponibility(
        self, row: pd.Series, age_range: list[str]
    ) -> list[str]:
        ages = [age for age in age_range if row[age] == "X" or row[age] == "x"]

        return ages

    def set_professional_use_case(self, use_case: pd.DataFrame) -> pd.DataFrame:
        # logger.info("[BACKEND] Setting PROFESSIONAL data rules")
        age_range = config.AGE_RANGE
        projects = config.PROJECTS
        use_case["RegraProfissional"]["professional_age_range"] = use_case[
            "RegraProfissional"
        ].apply(lambda x: self.age_range_disponibility(x, age_range), axis=1)

        use_case["LocalProfissional"]["professional_available_places"] = use_case[
            "LocalProfissional"
        ].apply(lambda x: self.local_disponibility(x, projects), axis=1)

        use_case["DisponProfissional"]["professional_hours"] = use_case[
            "DisponProfissional"
        ].apply(self.format_disponibility, axis=1)

        return use_case

    def consolidate_professionals_table(
        self, path
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        logger.info("[BACKEND] Reading PROFESSIONALS DATA")
        use_case: pd.DataFrame = self.read_xlsx(path)

        professional_consolidated_table: pd.DataFrame = pd.DataFrame()

        use_case: pd.DataFrame = self.set_professional_use_case(use_case)

        # logger.info("[BACKEND] Merging Professional tables")
        pre_professional: pd.DataFrame = pd.merge(
            use_case["RegraProfissional"],
            use_case["LocalProfissional"],
            on=["profissional"],
            how="inner",
        )

        use_case["DisponProfissional"]["profissional"] = use_case["DisponProfissional"][
            "profissional"
        ].ffill()

        professional: pd.DataFrame = pd.merge(
            pre_professional,
            use_case["DisponProfissional"],
            on=["profissional"],
            how="inner",
        )

        professional_consolidated_table: pd.DataFrame = professional.loc[
            :,
            [
                "profissional",
                "tipo",
                "horas_semana",
                "professional_age_range",
                "dia_semana",
                "professional_hours",
            ],
        ]

        return professional, professional_consolidated_table

    def get_dicts(
        self,
        patients_pre_consolidated_table: pd.DataFrame,
        patients_consolidated_table: pd.DataFrame,
        professional_pre_consolidated_table: pd.DataFrame,
        professional_consolidated_table: pd.DataFrame,
    ) -> Tuple[dict, dict, dict]:

        patient_age_range: pd.DataFrame = (
            patients_consolidated_table[["paciente", "patient_age_range"]]
            .drop_duplicates()
            .reset_index(drop=True)
        )

        professional_age_range_list: pd.DataFrame = (
            professional_consolidated_table[["profissional", "professional_age_range"]]
            .drop_duplicates(subset="profissional")
            .reset_index(drop=True)
        )

        logger.info("[BACKEND] ZPR Constructor")
        combination_dict = {
            (paciente["paciente"], profissional["profissional"]): (
                1
                if paciente["patient_age_range"]
                in profissional["professional_age_range"]
                else 0
            )
            for _, paciente in patient_age_range.iterrows()
            for _, profissional in professional_age_range_list.iterrows()
        }

        logger.info("[BACKEND] Patient Disponibility Constructor")
        disponibility_patients = {
            (paciente["paciente"], (paciente["dia_semana"], d), local): (
                1
                if (
                    (str(paciente[local]).lower() == "x")
                    and ((str(paciente[d]).lower() == "x"))
                )
                else 0
            )
            for _, paciente in patients_pre_consolidated_table.iterrows()
            for d in config.AVAILABLE_HOURS
            for local in config.PROJECTS
        }

        logger.info("[BACKEND] Professional disponibility Constructor")
        disponibility_professionals = {
            (professionals["profissional"], (professionals["dia_semana"], d), local): (
                1
                if (
                    (str(professionals[local]).lower() == "x")
                    and ((str(professionals[d]).lower() == "x"))
                )
                else 0
            )
            for _, professionals in professional_pre_consolidated_table.iterrows()
            for d in config.AVAILABLE_HOURS
            for local in config.PROJECTS
        }

        return combination_dict, disponibility_patients, disponibility_professionals

    def handle_input(self, path: str) -> pd.DataFrame:
        patients_pre_consolidated_table, patients_consolidated_table = (
            self.consolidate_patients_table(path=path)
        )

        professional_pre_consolidated_table, professional_consolidated_table = (
            self.consolidate_professionals_table(path=path)
        )

        combination_dict, disponibility_patients, disponibility_professionals = (
            self.get_dicts(
                patients_pre_consolidated_table,
                patients_consolidated_table,
                professional_pre_consolidated_table,
                professional_consolidated_table,
            )
        )

        return combination_dict, disponibility_patients, disponibility_professionals
