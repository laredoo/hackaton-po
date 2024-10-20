import logging
import pprint
import sys

from src.app.problem_instance.models import ProblemInstance, Sets
from src.app.validator.controller import ValidatorController
from src.core.factory.factory import Factory
from src.model.model import Model
from src.posprocessing.excel import Exporting
from src.utils.utils import read_sheet, save_sheet

pp = pprint.PrettyPrinter(indent=10)
logger = logging.getLogger(__name__)

PATH: str = r"C:\Users\luckr\OneDrive\Área de Trabalho\hackaton-po\docs\cenario_4.xlsx"


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
        local_list,
    ) = input_importer.handle_input(PATH)

    return (
        combination_dict,
        disponibility_patients,
        disponibility_professionals,
        professional_hours,
        local_list,
    )


def validate_input(factory: Factory, use_cases: dict):
    validator_controller: ValidatorController = factory.get_validator_controller(
        path=PATH, use_cases=use_cases
    )

    error = validator_controller.validate_input()

    if error:
        exit(500)


def preprocess_data(factory: Factory) -> ProblemInstance:
    (
        combination_dict,
        disponibility_patients,
        disponibility_professionals,
        professional_hours,
        local_list,
    ) = get_parameters(factory)

    problem_instance_controller: ProblemInstance = factory.problem_instance_controller(
        local_list,
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

    return problem_instance


def run_model(problem_instance: ProblemInstance):
    model = Model(problem_instance)
    model.create_variables()
    model.create_constraints()
    model.solve()
    model_data = model.export_result()

    return model_data


def posprocessing(
    model_data: list[list], problem_instance: ProblemInstance, use_cases: dict
):

    schedule_table = Exporting.create_table(
        model_data, problem_instance.sets.hours, problem_instance.sets.days
    )

    solution = Exporting.create_solution(model_data)

    use_cases["Solução"] = solution
    use_cases["schedule_table"] = schedule_table

    save_sheet("teste_unisoma.xlsx", use_cases)


def main():
    use_cases: dict = read_sheet(PATH)

    factory = create_factory()

    validate_input(factory, use_cases)

    problem_instance: ProblemInstance = preprocess_data(factory=factory)

    lista_dados = run_model(problem_instance=problem_instance)

    model_data = run_model(problem_instance=problem_instance)

    posprocessing(model_data, problem_instance, use_cases)


if __name__ == "__main__":
    # logger setup
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler("debug.log"), logging.StreamHandler(sys.stdout)],
    )

    # main function
    main()

    logger.info("Execution finished")
