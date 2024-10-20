import pandas as pd


class Exporting:
    def __init__(self):
        pass

    @staticmethod
    def create_table(lista_dados: list[list], hours: list[str], days: list[str]):
        df = pd.DataFrame(index=days, columns=hours)

        for lista in lista_dados:
            df.fillna("", inplace=True)
            print(df)
            df.loc[lista[2][0], lista[2][1]] += f"{lista[0]}-{lista[1]}-{lista[3]}   "

        return df
