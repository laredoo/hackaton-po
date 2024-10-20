class Config:
    DEFAULT_LANGUAGE: str = "pt-br"

    PROJECTS: list[str] = [
        "PROJETO ARRASTÃO",
        "LAR SÍRIO",
        "INSTITUTO BORBOLETA AZUL",
        "ASA - GAETANO E CARMELA",
        "ASA - PÁSSAROS",
        "ASA - SANTA MÔNICA",
        "ASA - PRIMAVERA",
        "ASA - SÃO JOSÉ",
        "virtual_epsi",
    ]

    AGE_RANGE: list[str] = ["infantil", "adolescente", "adulto"]

    AVAILABLE_HOURS: list[str] = [
        "hr_8",
        "hr_9",
        "hr_10",
        "hr_11",
        "hr_12",
        "hr_13",
        "hr_14",
        "hr_15",
        "hr_16",
        "hr_17",
        "hr_18",
        "hr_19",
        "hr_20",
    ]

    VALIDATION_ERROR: bool = False

    DAYS: list[str] = ["seg", "ter", "qua", "qui", "sex", "sáb"]

    PATH: str = (
        r"C:\Users\luckr\OneDrive\Área de Trabalho\hackaton-po\docs\cenario_1.xlsx"
    )


config: Config = Config()
