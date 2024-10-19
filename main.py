from src.core.factory.factory import Factory

PATH: str = r"C:\Users\luckr\OneDrive\Área de Trabalho\hackaton-po\docs\cenario_1.xlsx"


def create_factory() -> Factory:
    return Factory()


def main():
    factory = create_factory()
    input_importer = factory.get_model_import_repository()
    table = input_importer.handle_input(PATH)
    return table


if __name__ == "__main__":
    main()
