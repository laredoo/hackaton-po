import pulp
import logging
from src.app.problem_instance.models import ProblemInstance, Sets

logger = logging.getLogger(__name__)


class Model:
    def __init__(self, ProblemInstance: ProblemInstance):
        self.instance = ProblemInstance
        self.model = pulp.LpProblem("DesafioUnisoma", pulp.LpMaximize)

    def create_variables(self) -> None:
        patients = self.instance.sets.patients
        professionals = self.instance.sets.professionals
        places = self.instance.sets.places
        schedule = self.instance.sets.schedules
        logger.info("[Model] Generating variables")
        self.x = pulp.LpVariable.dicts(
            "X", (patients, professionals, schedule, places), cat="Binary"
        )

    def create_constraints(self) -> None:
        # Sets
        patients = self.instance.sets.patients
        professionals = self.instance.sets.professionals
        places = self.instance.sets.places
        schedule = self.instance.sets.schedules
        presencials_locals = [
            p for p in self.instance.sets.places if p != "virtual_epsi"
        ]
        days = self.instance.sets.days
        list_days = [[(i, j) for (i, j) in schedule if i == d] for d in days]

        # Parameters
        dispP = self.instance.parameter.patients_disponibility
        dispR = self.instance.parameter.professional_disponibility
        z = self.instance.parameter.zbr
        O = self.instance.parameter.professional_hours
        logger.info("[Model] Generating Objective Function")
        # Objective Funtion
        self.model += pulp.lpSum(
            self.x[p][r][h][l]
            for p in patients
            for r in professionals
            for h in schedule
            for l in places
        )
        # Constraint 1
        logger.info("[Model] Generating constraints (1)")
        for p in patients:
            self.model += (
                pulp.lpSum(
                    self.x[p][r][h][l]
                    for r in professionals
                    for h in schedule
                    for l in places
                )
                <= 1
            )
        # Constraint 2
        logger.info("[Model] Generating constraints (2) and (3)")
        for r in professionals:
            for h in schedule:
                self.model += (
                    pulp.lpSum(self.x[p][r][h][l] for p in patients for l in places)
                    <= 1
                )

                for p in patients:
                    for l in places:
                        # Constraint 3
                        self.model += (
                            self.x[p][r][h][l]
                            <= dispP[p, h, l] * dispR[r, h, l] * z[p, r]
                        )

        # Constraint 4
        logger.info("[Model] Generating constraint (4)")
        for r in professionals:
            self.model += (
                pulp.lpSum(
                    self.x[p][r][h][l]
                    for p in patients
                    for l in places
                    for h in schedule
                )
                <= O[r]
            )

        # Constraint 5
        logger.info("[Model] Generating constraint (5)")

        for D in list_days:
            for r in professionals:
                self.model += (
                    pulp.lpSum(
                        self.x[p][r][h][l]
                        for p in patients
                        for h in D
                        for l in presencials_locals
                    )
                    <= 1
                )

    def solve(self) -> None:
        logger.info("[Model] Calling Solver CBC(COIN BRANCH AND CUT)")
        self.model.solve(pulp.PULP_CBC_CMD(timeLimit=600, msg=False))
        return

    def export_result(self) -> None:
        model_data = [
            [p, r, h, l]
            for r in self.instance.sets.professionals
            for h in self.instance.sets.schedules
            for p in self.instance.sets.patients
            for l in self.instance.sets.places
            if pulp.value(self.x[p][r][h][l]) == 1
        ]
        return model_data
