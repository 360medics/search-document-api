from datetime import date
from typing import Literal, List
from pydantic import BaseModel


class Consulation(BaseModel):
    Text: str = None
    Prescription: str = None
    Resultat_consultation: str = None
    Accident_travail: str = None
    Biometrie: str = None
    Biologie: str = None
    Date_consultation: date = None


class MedGDocument(BaseModel):
    DDN: date
    Consultations: List[Consulation]
    sex: Literal["Homme", "Femme"]
