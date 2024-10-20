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
            df.loc[list[2][0], list[2][1]] += f"{list[0]}-{list[1]}-{list[3]}   "
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

    # def create_summary(instance: ProblemInstance, model_data: list[list]):

    #     patients = instance.sets.patients
    #     professionals = instance.sets.professionals
    #     places = instance.sets.places

    #     O = instance.parameter.professional_hours
    #     n_alocations = len(model_data)

    #     alocation_percentage = n_alocations / len(patients)
    #     df_alocation_percentage = pd.DataFrame(pd.Series(alocation_percentage))
    #     print(df_alocation_percentage)
    #     print(alocation_percentage)

    #     alocations = pd.DataFrame(
    #         model_data, columns=["Paciente", "professionals", "Intervalo", "Lugar"]
    #     )

    #     dict_r = alocations["professionals"].value_counts().to_dict()
    #     dict_r = {key: value / O[key] for key, value in dict_r.items()}

    #     for r in professionals:
    #         if r not in dict_r:
    #             dict_r[r] = 0
    #     print(dict_r)

    #     dict_l = alocations["Lugar"].value_counts().to_dict()
    #     dict_l = {key: value / n_alocations for key, value in dict_l.items()}
    #     for l in places:
    #         if l not in dict_l:
    #             dict_l[l] = 0
    #     print(dict_l)

    #     dict_p =  alocations["Paciente"].value_counts().to_dict()
    #     non_alocated_p = [p for p in patients if p not in dict_p]

    #     return

    def create_summary(instance, model_data: list[list]):
        patients = instance.sets.patients
        professionals = instance.sets.professionals
        places = instance.sets.places

        O = instance.parameter.professional_hours
        n_alocations = len(model_data)

        alocation_percentage = n_alocations / len(patients)

        alocations = pd.DataFrame(
            model_data, columns=["Paciente", "professionals", "Intervalo", "Lugar"]
        )

        dict_r = alocations["professionals"].value_counts().to_dict()
        dict_r = {key: value / O[key] for key, value in dict_r.items()}
        for r in professionals:
            if r not in dict_r:
                dict_r[r] = "Não alocado"

        dict_l = alocations["Lugar"].value_counts().to_dict()
        dict_l = {key: value / n_alocations for key, value in dict_l.items()}
        for l in places:
            if l not in dict_l:
                dict_l[l] = 0

        dict_p = alocations["Paciente"].value_counts().to_dict()
        non_alocated_p = [p for p in patients if p not in dict_p]

        summary_data = []

        summary_data.append(
            ["Porcentagem dos pacientes atendidos: ", alocation_percentage]
        )

        summary_data.append(["", ""])

        summary_data.append(
            ["Profissional", "Porcentagem Ocupada de Carga Horária"]
        )  # Linha em branco

        for professional, value in dict_r.items():
            summary_data.append([professional, value])

        summary_data.append(["", ""])
        for p in non_alocated_p:
            summary_data.append([p, "Paciente sem Consulta"])

        summary_data.append(["", ""])
        summary_data.append(["Lugares", "Porcentagem de Atendimentos"])

        for place, value in dict_l.items():
            summary_data.append([place, value])

        df_summary = pd.DataFrame(summary_data, columns=["Descrição", "Valor"])

        return df_summary
