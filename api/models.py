from sqlalchemy import Column, Integer, String, Boolean, Float, Date

from api.database import Base

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    age = Column(Integer, nullable=True)
    taille = Column(Float, nullable=True)
    poids = Column(Float, nullable=True)
    sexe = Column(String, nullable=True)
    sport_licence = Column(Boolean, nullable=True)
    niveau_etude = Column(String, nullable=True)
    region = Column(String, nullable=True)
    smoker = Column(Boolean, nullable=True)
    revenu_estime_mois = Column(Float, nullable=True)
    situation_familiale = Column(String, nullable=True)
    historique_credits = Column(Float, nullable=True)
    risque_personnel = Column(Float, nullable=True)
    score_credit = Column(Float, nullable=True)
    loyer_mensuel = Column(Float, nullable=True)
    montant_pret = Column(Float, nullable=True)
    date_creation_compte = Column(String, nullable=True) # Changed to String for pandas compatibility
    nb_enfants = Column(Integer, nullable=True)
    quotient_caf = Column(Float, nullable=True)
