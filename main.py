import logging
import pprint
import sys

from src.app.problem_instance.models import ProblemInstance, Sets
from src.core.factory.factory import Factory
from src.model.model import Model

pp = pprint.PrettyPrinter(indent=10)
logger = logging.getLogger(__name__)

PATH: str = (
    r"C:\Users\danin\Desktop\Projects\Desafio Unisoma\hackaton-po\docs\cenario_3.xlsx"
)


def create_factory() -> Factory:
    return Factory()


def get_parameters(factory: Factory) -> tuple[dict, dict, dict, dict]:
    input_importer = factory.get_model_import_controller()
    logger.info("[BACKEND] Generating Parameters")
    (
        combination_dict,
        disponibility_patients,
        disponibility_professionals,
        professional_hours,
    ) = input_importer.handle_input(PATH)
    # pp.pprint(disponibility_patients)
    return (
        combination_dict,
        disponibility_patients,
        disponibility_professionals,
        professional_hours,
    )


def main():
    factory = create_factory()

    (
        combination_dict,
        disponibility_patients,
        disponibility_professionals,
        professional_hours,
    ) = get_parameters(factory)

    problem_instance_controller = factory.problem_instance_controller(
        combination_dict,
        disponibility_patients,
        disponibility_professionals,
        professional_hours,
    )

    sets: Sets = problem_instance_controller.get_sets(
        use_case=factory.get_model_import_controller().read_xlsx(PATH)
    )

    problem_instance: ProblemInstance = (
        problem_instance_controller.get_problem_instance(sets)
    )
    model = Model(problem_instance)
    model.create_variables()
    model.create_constraints()
    model.solve()
    model.export_result()

    return problem_instance.parameter.zbr


if __name__ == "__main__":
    # logger setup
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler("debug.log"), logging.StreamHandler(sys.stdout)],
    )

    # main function
    main()
