import logging
import pprint
import sys

from src.core.factory.factory import Factory

pp = pprint.PrettyPrinter(indent=10)

PATH: str = r"C:\Users\luckr\OneDrive\Área de Trabalho\hackaton-po\docs\cenario_1.xlsx"


def create_factory() -> Factory:
    return Factory()


def main():
    factory = create_factory()
    input_importer = factory.get_model_import_repository()
    combination_dict, disponibility_patients, disponibility_professionals = (
        input_importer.handle_input(PATH)
    )
    pp.pprint(disponibility_patients)
    return combination_dict, disponibility_patients, disponibility_professionals


if __name__ == "__main__":
    # logger setup
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler("debug.log"), logging.StreamHandler(sys.stdout)],
    )

    # main function
    main()
