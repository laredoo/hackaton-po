import pulp 

class Model:
    
    def __init__(self, ProblemInstance):
        self.instance = ProblemInstance
        

        self.model = pulp.LpProblem("Unisoma", pulp.LpMaximize)
        self.x = None
        pass

    def create_variables(self):

        pacientes = self.pacientes
        profisisional = self.profissional
        locais = self.locais
        interval = self.interval 
        
        self.x = pulp.LpVariable.dicts("X", (pacientes, profisisional, locais), cat='Binary')
        
        pass

    def create_constraints(self):
        
        # Constraint 1
        self.model += pulp.lpSum(self.x[p][r][h][l] for p in self.pacientes for r in self.profissional for h in self.interval for l in self.locais) <= 1
        
        # Constraint 2
        for r in self.profissional:
            for h in self.interval:
                self.model += pulp.lpSum(self.x[p][r][h][l] for p in self.pacientes for l in self.locais) <= 1
        
                for p in self.pacientes:
                    for l in self.locais:
                        # Constraint 3
                        self.model += self.x[p][r][h][l] <= self.dispP[p,h,l] * self.dispR[r,h,l] * self.z[p,r]
                        
        # Constraint 4
        for r in self.profissional:
            self.model += pulp.lpSum(self.x[p][r][h][l] for p in self.pacientes for l in self.locais for h in self.interval) <= self.O[r]
    
        # Constraint 5
        for h in self.locais_presenciais:
            for l in self.locais_presenciais:
            self.model += pulp.lpSum(self.x[p][r][h][l] for p in self.pacientes for l in self.locais for h in self.interval) <= self.O[r]
        
    
        pass
    

    
    def solve(self):
        pass
    
    def export_result(self):
        pass

