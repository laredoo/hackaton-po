import pulp


class Model:
    def __init__(self, ProblemInstance):
        self.instance = ProblemInstance
        self.model = pulp.LpProblem("DesafioUnisoma", pulp.LpMaximize)

    def create_variables(self) -> None:
        patients = self.instance.patients
        professionals = self.instance.professionals
        places = self.instance.places
        interval = self.instance.interval
        self.x = pulp.LpVariable.dicts(
            "X", (patients, professionals, interval, places), cat="Binary"
        )

    def create_constraints(self) -> None:

        patients = self.instance.patients
        professionals = self.instance.professionals
        places = self.instance.places
        interval = self.instance.interval
        dispP = self.instance.dispP
        dispR = self.instance.dispR
        z = self.instance.z
        O = self.instance.O
        locais_presenciais = self.instance.locais_presenciais
        dias = self.instance.dias

        # Objective Funtion
        self.model += pulp.lpSum(
            self.x[p][r][h][l]
            for p in patients
            for r in professionals
            for h in interval
            for l in places
        )

        # Constraint 1
        for p in patients:
            self.model += (
                pulp.lpSum(
                    self.x[p][r][h][l]
                    for r in professionals
                    for h in interval
                    for l in places
                )
                <= 1
            )
        # Constraint 2
        for r in professionals:
            for h in interval:
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
                    for h in interval
                )
                <= O[r]
            )

        # Constraint 5
        for D in dias:
            for r in professionals:
                self.model += (
                    pulp.lpSum(
                        self.x[p][r][h][l]
                        for p in patients
                        for h in D
                        for l in locais_presenciais
                    )
                    <= 1
                )

    def solve(self) -> None:
        self.model.solve(pulp.PULP_CBC_CMD(timeLimit=20, msg=True))
        return

    def export_result(self) -> None:

        for r in self.instance.professionals:
            for h in self.instance.interval:
                for p in self.instance.patients:
                    for l in self.instance.places:
                        if pulp.value(self.x[p][r][h][l]) == 1:
                            print(f"Cliente {p}, Profissional {r}, Hora {h}, Local {l}")

        lista_dados = [
            [p, r, h, l]
            for r in self.instance.professionals
            for h in self.instance.interval
            for p in self.instance.patients
            for l in self.instance.places
            if pulp.value(self.x[p][r][h][l]) == 1
        ]

        return lista_dados


class ProblemInstance:
    def __init__(self):
        # Larger instance for testing with full parameter availability
        self.patients = ["P1", "P2", "P3", "P4"]
        self.professionals = ["R1", "R2", "R3"]
        self.places = ["L1", "L2"]
        self.interval = ["H1", "H2", "H3"]
        self.dispP = {
            ("P1", "H1", "L1"): 0,
            ("P1", "H1", "L2"): 1,
            ("P1", "H2", "L1"): 1,
            ("P1", "H2", "L2"): 1,
            ("P1", "H3", "L1"): 0,
            ("P1", "H3", "L2"): 1,
            ("P2", "H1", "L1"): 1,
            ("P2", "H1", "L2"): 0,
            ("P2", "H2", "L1"): 0,
            ("P2", "H2", "L2"): 0,
            ("P2", "H3", "L1"): 0,
            ("P2", "H3", "L2"): 0,
            ("P3", "H1", "L1"): 1,
            ("P3", "H1", "L2"): 1,
            ("P3", "H2", "L1"): 1,
            ("P3", "H2", "L2"): 1,
            ("P3", "H3", "L1"): 1,
            ("P3", "H3", "L2"): 1,
            ("P4", "H1", "L1"): 1,
            ("P4", "H1", "L2"): 1,
            ("P4", "H2", "L1"): 1,
            ("P4", "H2", "L2"): 1,
            ("P4", "H3", "L1"): 1,
            ("P4", "H3", "L2"): 0,
        }
        self.dispR = {
            ("R1", "H1", "L1"): 1,
            ("R1", "H1", "L2"): 0,
            ("R1", "H2", "L1"): 1,
            ("R1", "H2", "L2"): 1,
            ("R1", "H3", "L1"): 1,
            ("R1", "H3", "L2"): 1,
            ("R2", "H1", "L1"): 1,
            ("R2", "H1", "L2"): 1,
            ("R2", "H2", "L1"): 1,
            ("R2", "H2", "L2"): 1,
            ("R2", "H3", "L1"): 1,
            ("R2", "H3", "L2"): 1,
            ("R3", "H1", "L1"): 1,
            ("R3", "H1", "L2"): 1,
            ("R3", "H2", "L1"): 1,
            ("R3", "H2", "L2"): 1,
            ("R3", "H3", "L1"): 1,
            ("R3", "H3", "L2"): 1,
        }
        self.z = {
            ("P1", "R1"): 1,
            ("P1", "R2"): 0,
            ("P1", "R3"): 1,
            ("P2", "R1"): 1,
            ("P2", "R2"): 1,
            ("P2", "R3"): 0,
            ("P3", "R1"): 1,
            ("P3", "R2"): 1,
            ("P3", "R3"): 1,
            ("P4", "R1"): 0,
            ("P4", "R2"): 1,
            ("P4", "R3"): 1,
        }
        self.O = {"R1": 3, "R2": 2, "R3": 2}
        self.dias = [["H1", "H2"], ["H3"]]
        self.locais_presenciais = ["L1", "L2"]


def main():
    # Create an instance of ProblemInstance
    problem_instance = ProblemInstance()

    # Create an instance of Model with the problem instance
    model = Model(problem_instance)

    # Create variables, constraints, and solve the model
    model.create_variables()
    model.create_constraints()
    model.solve()

    # Export the result
    data = model.export_result()
    table = exporting.create_table(data)


if __name__ == "__main__":
    main()
