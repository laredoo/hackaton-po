import pandas as pd

from src.app.validator.validator import Validator


class ValidatorController:
    def __init__(self, validator: Validator):
        self.validator = validator

    def validate_input(self):
        message_list = []

        # Checking age
        patient_age_message, error = self.validator.check_patient_age()
        message_list.append(patient_age_message)

        return message_list, error
