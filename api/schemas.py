from pydantic import BaseModel
from typing import Literal

Region = Literal[
    'Auvergne-Rhône-Alpes', 
    'Bretagne', 
    'Corse', 
    'Hauts-de-France',
    'Île-de-France', 
    'Normandie', 
    'Occitanie', 
    'Provence-Alpes-Côte d\'Azur',
    ]
NiveauEtude = Literal[
    'bac+2', 
    'bac', 
    'master', 
    'doctorat', 
    'aucun',
    ]
Sexe = Literal['H','F']

class Client(BaseModel):
    age: int
    taille: float
    poids: float
    sexe: Sexe
    sport_licence: bool
    niveau_etude: NiveauEtude
    region: Region
    smoker: bool
    nationalite_francaise: bool
    revenu_estime_mois: int
