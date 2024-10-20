import pandas as pd


def read_sheet(path: str) -> dict:
    return pd.read_excel(path, sheet_name=None)


def save_sheet(path: str, use_cases: dict) -> None:

    with pd.ExcelWriter(path) as writer:
        for sheet_name, df in use_cases.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
