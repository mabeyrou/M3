from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

from api.config import DATABASE_URL

engine = create_engine(DATABASE_URL,
                       connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Générateur de session de base de données"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_db_tables():
    """Crée les tables de la base de données"""
    Base.metadata.create_all(bind=engine)

def clear_table(table_name):
    """Vide une table"""
    db = SessionLocal()
    try:
        db.execute(text(f"DELETE FROM {table_name}"))
        db.commit()
        print(f"🗑️  Table {table_name} vidée")
    except Exception as e:
        db.rollback()
        print(f"❌ Erreur lors du vidage: {e}")
        raise
    finally:
        db.close()
