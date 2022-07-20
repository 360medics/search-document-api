from datetime import datetime
from typing import Literal
from pydantic import BaseModel


class Consulation(BaseModel):
    input_text: str = None
    prescription: str = None
    resultat_consultation: str = None
    accident_travail: str = None
    biometrie: str = None
    biologie: str = None
    date_consultation: datetime = None


class MedGDocument(BaseModel):
    date_of_birth: datetime
    consultations: list[Consulation]
    gender: Literal["Homme", "Femme"]
