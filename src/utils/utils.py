import pandas as pd


def read_sheet(path: str) -> dict:
    return pd.read_excel(path, sheet_name=None)


def save_sheet(path: str) -> dict:
    pass
