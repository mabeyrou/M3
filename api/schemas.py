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
SituationFamiliale = Literal['veuf', 'marié', 'célibataire', 'divorcé']
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
    nationalité_francaise: bool
    revenu_estime_mois: int
    situation_familiale: SituationFamiliale
    historique_credits: float
    risque_personnel: float
    score_credit: float
    loyer_mensuel: float
    montant_pret: float
