from pydantic import BaseModel


class Parameter(BaseModel):
    zbr: dict
    patients_disponibility: dict
    professional_disponibility: dict
    professional_hours: dict


class Sets(BaseModel):
    patients: list
    professionals: list
    schedules: list
    places: list
    days: list
    hours: list


class ProblemInstance(BaseModel):
    parameter: Parameter
    sets: Sets
