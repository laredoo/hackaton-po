import pandas as pd


class exporting:
    def __init__(self):
        pass

    def create_table(
        self, lista_dados: list[list], colunas: list[str], linhas: list[str]
    ):
        df = pd.DataFrame(index=linhas, columns=colunas)

        for lista in lista_dados:
            df.at[lista[3][0], lista[3][1]] = f"{lista[0]}_{lista[1]}_{lista[2]}"

        return df
