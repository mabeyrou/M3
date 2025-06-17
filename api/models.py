from sqlalchemy import Column, Integer, String, Boolean, Float, Date
from .database import Base

class Loan(Base):
    __tablename__ = 'loans'
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String)
    prenom = Column(String)
    age = Column(Integer)
    taille = Column(Float)
    poids = Column(Float)
    sexe = Column(String)
    sport_licence = Column(Boolean)
    niveau_etude = Column(String)
    region = Column(String)
    smoker = Column(Boolean)
    nationalite_francaise = Column(Boolean)
    revenu_estime_mois = Column(Integer)
    situation_familiale = Column(String)
    historique_credits = Column(Float)
    risque_personnel = Column(Float)
    date_creation_compte = Column(Date)
    score_credit = Column(Float)
    loyer_mensuel = Column(Float)
    montant_pret = Column(Float)
