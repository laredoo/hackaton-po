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

    def create_summary(instance: ProblemInstance, model_data: list[list]):

        patients = instance.sets.patients
        professionals = instance.sets.professionals
        places = instance.sets.places
        schedule = instance.sets.schedules

        dispP = instance.parameter.patients_disponibility
        dispR = instance.parameter.professional_disponibility
        z = instance.parameter.zbr
        O = instance.parameter.professional_hours

        return
