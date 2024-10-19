import pandas as pd
from src.app.problem_instance.models import Parameter, ProblemInstance, Sets
from src.core.config import config


class ProblemInstanceController:
    def __init__(
        self,
        zbr,
        patients_disponibility,
        professional_disponibility,
        professional_hours,
    ):
        self.language = config.DEFAULT_LANGUAGE
        self.zbr = zbr
        self.patients_disponibility = patients_disponibility
        self.professional_disponibility = professional_disponibility
        self.professional_hours = professional_hours

    def get_parameter(self):
        return Parameter(
            **{"zbr": self.zbr},
            **{"patients_disponibility": self.patients_disponibility},
            **{"professional_disponibility": self.professional_disponibility},
            **{"professional hours": self.professional_hours},
        )

    def get_sets(self, use_case: pd.DataFrame):

        patients: list = list(use_case["IdadePaciente"]["paciente"].unique())

        professionals: list = list(
            use_case["RegraProfissional"]["profissional"].unique()
        )

        schedules: list = [(d, h) for d in config.DAYS for h in config.AVAILABLE_HOURS]

        places: list = config.PROJECTS

        days: list = config.DAYS
        return Sets(
            **{"patients": patients},
            **{"professionals": professionals},
            **{"schedules": schedules},
            **{"places": places},
            **{"days": days},
        )

    def get_problem_instance(self, sets: Sets):
        parameter: Parameter = self.get_parameter()
        return ProblemInstance(**{"parameter": parameter}, **{"sets": sets})
