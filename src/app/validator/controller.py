import logging
from openpyxl import load_workbook

from src.app.validator.validator import Validator

logger = logging.getLogger(__name__)


class ValidatorController:
    def __init__(self, validator: Validator, path: str):
        self.validator = validator
        self.path = path

    def limpar_aba_inconsistencias(self, aba="Inconsistência"):
        # Carrega o arquivo Excel com openpyxl
        workbook = load_workbook(self.path)

        if aba in workbook.sheetnames:
            sheet = workbook[aba]

            sheet.delete_rows(2, sheet.max_row)

            workbook.save(self.path)
            # logger.info(f"A aba '{aba}' foi limpa com sucesso.")
        else:
            logger.error(f"A aba '{aba}' não foi encontrada no arquivo.")
            exit(500)

    def validate_input(self):
        # clean Inconsistências tab before validate
        self.limpar_aba_inconsistencias()

        # Checking age
        logger.info("[VALIDATOR] Checking Patient Age")
        error = self.validator.check_patient_age()

        # Checking schedule
        logger.info("[VALIDATOR] Checking Schedule")
        error = self.validator.check_has_schedule()

        return error
