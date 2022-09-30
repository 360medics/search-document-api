from datetime import date
from typing import Literal
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
    Consultations: list[Consulation]
    sex: Literal["Homme", "Femme"]


class FRCP(BaseModel):
    DDN: str = None
    DateRCP: str = None
    DatePrelevement: str = None
    NaturePrelevement: str = None
    ResiduTumoralApresChirurgie: str = None
    T: str = None
    N: str = None
    M: str = None
    Histologie: str = None
    MotifRCP: str = None
    ATCD: str = None
    HDM: str = None
    Question: str = None
    OMS: str = None
    Decouverte: str = None
    Patho: str = None
    PhaseMaladie: str = None
    DPD: str = None
    TypeTT: str = None
    DetailTT: str = None
    PhaseTT: str = None
    TypeTT2: str = None
    TypeTT3: str = None
