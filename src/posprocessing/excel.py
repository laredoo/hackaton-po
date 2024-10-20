import pandas as pd
from datetime import datetime


class Exporting:
    def __init__(self):
        pass

    @staticmethod
    def create_table(model_data: list[list], hours: list[str], days: list[str]):
        df = pd.DataFrame(index=days, columns=hours)

        for list in model_data:
            df.fillna("", inplace=True)
            print(df)
            df.loc[list[2][0], list[2][1]] += f"{list[0]}-{list[1]}-{list[3]}   "

        return df

    def create_solution(model_data: list[list]):
        columns_name: list = [
            "paciente",
            "profissional",
            "dia_semana",
            "hora",
            "local",
            "dt_atualizacao",
        ]
        df = pd.DataFrame(model_data, columns=columns_name)
        print(datetime.now())
        pass
