from sqlalchemy import Column, Integer, String, Boolean, Float
from .database import Base

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True, index=True)
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
    score_credit = Column(Float)
    loyer_mensuel = Column(Float)
    montant_pret = Column(Float)
