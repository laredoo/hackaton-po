import logging
import sys
import os
import time
from src.app.problem_instance.models import ProblemInstance, Sets
from src.app.validator.controller import ValidatorController
from src.core.factory.factory import Factory
from src.model.model import Model
from src.posprocessing.excel import Exporting
from src.utils.utils import read_sheet, save_sheet

logger = logging.getLogger(__name__)


def create_factory() -> Factory:
    return Factory()


def get_parameters(factory: Factory, path_excel: str) -> tuple[dict, dict, dict, dict]:
    input_importer = factory.get_model_import_controller()
    logger.info("[BACKEND] Generating Parameters")
    (
        combination_dict,
        disponibility_patients,
        disponibility_professionals,
        professional_hours,
        local_list,
    ) = input_importer.handle_input(path_excel)

    return (
        combination_dict,
        disponibility_patients,
        disponibility_professionals,
        professional_hours,
        local_list,
    )


def validate_input(factory: Factory, use_cases: dict, path: str):
    validator_controller: ValidatorController = factory.get_validator_controller(
        path=path, use_cases=use_cases
    )

    error = validator_controller.validate_input()

    # if error:
    #     exit(500)


def preprocess_data(factory: Factory, path_excel: str) -> ProblemInstance:
    (
        combination_dict,
        disponibility_patients,
        disponibility_professionals,
        professional_hours,
        local_list,
    ) = get_parameters(factory, path_excel)

    problem_instance_controller: ProblemInstance = factory.problem_instance_controller(
        local_list,
        combination_dict,
        disponibility_patients,
        disponibility_professionals,
        professional_hours,
    )

    sets: Sets = problem_instance_controller.get_sets(
        use_case=factory.get_model_import_controller().read_xlsx(path_excel)
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
    model_data: list[list],
    problem_instance: ProblemInstance,
    use_cases: dict,
    path_excel: str,
):

    schedule_table = Exporting.create_table(
        model_data, problem_instance.sets.hours, problem_instance.sets.days
    )
    # path_excel, _ = os.path.splitext(path_excel)
    # path_excel = f"{path_excel}_output"
    solution = Exporting.create_solution(model_data)
    logger.info("[Results] Exporting Solution into Excel file ")
    use_cases["Solução"] = solution
    logger.info("[Results] Exporting Schedule table into Excel")
    use_cases["schedule_table"] = schedule_table

    save_sheet(path_excel, use_cases, ["Solução", "schedule_table"])


def main(path_excel: str):

    use_cases: dict = read_sheet(path_excel)

    factory = create_factory()

    validate_input(factory, use_cases, path_excel)

    problem_instance: ProblemInstance = preprocess_data(
        factory=factory, path_excel=path_excel
    )

    model_data = run_model(problem_instance=problem_instance)

    posprocessing(model_data, problem_instance, use_cases, path_excel)


if __name__ == "__main__":
    # logger setup
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler("debug.log"), logging.StreamHandler(sys.stdout)],
    )
    path_excel = input("Please provide the path to the Excel file: ")

    # main function
    main(path_excel)

    while True:
        user_input = input("Press '0' to exit the application...\n")
        if user_input == "0":
            break

    logger.info("Execution finished")
