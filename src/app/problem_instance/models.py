from pydantic import BaseModel


class Parameter(BaseModel):
    zbr: dict
    patients_disponibility: dict
    professional_disponibility: dict


class Sets(BaseModel):
    patients: list
    professionals: list
    schedules: list
    places: list


class ProblemInstance(BaseModel):
    parameter: Parameter
    sets: Sets
