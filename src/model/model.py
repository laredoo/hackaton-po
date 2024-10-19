import pulp
from src.app.problem_instance.models import ProblemInstance, Sets


class Model:
    def __init__(self, ProblemInstance: ProblemInstance):
        self.instance = ProblemInstance
        self.model = pulp.LpProblem("DesafioUnisoma", pulp.LpMaximize)

    def create_variables(self) -> None:
        patients = self.instance.sets.patients
        professionals = self.instance.sets.professionals
        places = self.instance.sets.places
        schedule = self.instance.sets.schedules
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
        # Parameters
        dispP = self.instance.parameter.patients_disponibility
        dispR = self.instance.parameter.professional_disponibility
        z = self.instance.parameter.zbr
        O = self.instance.parameter.professional_hours

        # Objective Funtion
        self.model += pulp.lpSum(
            self.x[p][r][h][l]
            for p in patients
            for r in professionals
            for h in schedule
            for l in places
        )

        # Constraint 1
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
        for r in professionals:
            self.model += (
                pulp.lpSum(
                    self.x[p][r][h][l]
                    for p in patients
                    for h in schedule
                    for l in presencials_locals
                )
                <= 1
            )

    def solve(self) -> None:
        self.model.solve(pulp.PULP_CBC_CMD(timeLimit=20, msg=True))
        return

    def export_result(self) -> None:

        for r in self.instance.sets.professionals:
            for h in self.instance.sets.schedules:
                for p in self.instance.sets.patients:
                    for l in self.instance.sets.places:
                        if pulp.value(self.x[p][r][h][l]) == 1:
                            print(
                                f"Cliente {p}, Profissional {r}, Hora {h}, Local {l}\n"
                            )

        lista_dados = [
            [p, r, h, l]
            for r in self.instance.sets.professionals
            for h in self.instance.sets.schedules
            for p in self.instance.sets.patients
            for l in self.instance.sets.places
            if pulp.value(self.x[p][r][h][l]) == 1
        ]
        return lista_dados
