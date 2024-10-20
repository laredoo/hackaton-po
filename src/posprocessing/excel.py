import pandas as pd
from datetime import datetime

from src.app.problem_instance.models import ProblemInstance


class Exporting:
    def __init__(self):
        pass

    @staticmethod
    def create_table(model_data: list[list], hours: list[str], days: list[str]):
        df = pd.DataFrame(index=days, columns=hours)

        for list in model_data:
            df = df.fillna("")
            df.loc[list[2][0], list[2][1]] += f"{list[0]}-{list[1]}-{list[3]}  "
        df = df.reset_index().rename(columns={"index": "Dias/Horas"})

        return df

    def create_solution(model_data: list[list]):
        columns_name: list = [
            "paciente",
            "profissional",
            "intervalo",
            "local",
        ]

        df = pd.DataFrame(model_data, columns=columns_name)

        df[["dia de semana", "hora"]] = df["intervalo"].apply(pd.Series)
        df.drop(columns=["intervalo"], inplace=True)
        df["df_atualizacao"] = datetime.now()

        return df

    def create_summary(instance, model_data: list[list]):
        patients = instance.sets.patients
        professionals = instance.sets.professionals
        places = instance.sets.places

        O = instance.parameter.professional_hours
        n_alocations = len(model_data)

        alocation_percentage = n_alocations / len(patients)

        alocations = pd.DataFrame(
            model_data, columns=["Paciente", "Profissional", "Intervalo", "Lugar"]
        )

        # Porcentagem de carga horária ocupada por profissional
        dict_r = alocations["Profissional"].value_counts().to_dict()
        dict_r = {key: value / O[key] for key, value in dict_r.items()}
        for r in professionals:
            if r not in dict_r:
                dict_r[r] = "Não alocado"

        # Porcentagem de atendimentos por lugar
        dict_l = alocations["Lugar"].value_counts().to_dict()
        dict_l = {key: value / n_alocations for key, value in dict_l.items()}
        for l in places:
            if l not in dict_l:
                dict_l[l] = 0

        # Pacientes sem consulta
        dict_p = alocations["Paciente"].value_counts().to_dict()
        non_alocated_p = [p for p in patients if p not in dict_p]

        summary_data = []

        # Adiciona as porcentagens de pacientes atendidos
        summary_data.append(
            ["Porcentagem de Pacientes Atendidos", f"{alocation_percentage:.2%}"]
        )

        summary_data.append(["", ""])  # Linha em branco

        # Adiciona as porcentagens de profissionais ocupados
        summary_data.append(["Profissional", "Porcentagem Ocupada da Carga Horária"])
        for professional, value in dict_r.items():
            if isinstance(
                value, float
            ):  # Formata como porcentagem apenas se for número
                value = f"{value:.2%}"
            summary_data.append([professional, value])

        summary_data.append(["", ""])  # Linha em branco para separar seções

        # Lista pacientes sem consulta
        if non_alocated_p:
            summary_data.append(["Pacientes Sem Consulta", ""])
            for p in non_alocated_p:
                summary_data.append([p, ""])

        summary_data.append(["", ""])  # Linha em branco

        # Adiciona porcentagens de atendimentos por local
        summary_data.append(["Lugar", "Porcentagem de Atendimentos"])
        for place, value in dict_l.items():
            summary_data.append([place, f"{value:.2%}"])

        # Cria o DataFrame final
        df_summary = pd.DataFrame(summary_data, columns=["Descrição", "Valor"])

        return df_summary
