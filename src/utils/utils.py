import pandas as pd


def read_sheet(path: str) -> dict:
    return pd.read_excel(path, sheet_name=None)


def save_sheet(path: str, use_cases: dict, tabs: list = None) -> None:

    for tab in tabs:
        if tab == "Tabela de Horários" or "Solução":
            with pd.ExcelWriter(
                path, engine="openpyxl", mode="a", if_sheet_exists="overlay"
            ) as writer:
                use_cases[tab].to_excel(
                    writer,
                    sheet_name=tab,
                    index=False,
                    header=True,
                )
        else:
            with pd.ExcelWriter(
                path, engine="openpyxl", mode="a", if_sheet_exists="overlay"
            ) as writer:
                use_cases[tab].to_excel(
                    writer,
                    sheet_name=tab,
                    index=False,
                    header=False,
                )
