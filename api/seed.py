import pandas as pd
from sqlalchemy import text
from .database import engine, SessionLocal, create_db_tables
from .models import *

def import_csv_to_db(csv_path, table_name, if_exists='replace'):
    """
    Importe un CSV directement en base
    
    Args:
        csv_path: Chemin vers le fichier CSV
        table_name: Nom de la table en base
        if_exists: 'append', 'replace', ou 'fail'
    """
    try:
        df = pd.read_csv(csv_path)
        df.insert(0, 'id', range(1, len(df) + 1))
        colonnes_bool = ['smoker', 'sport_licence', 'nationalite_francaise']
        df = df.assign(**{col: df[col].str.lower().map(convert_to_bool) for col in colonnes_bool})
        df = df.drop(columns=['nom', 'prenom', 'date_creation_compte'])
        
        df.to_sql(
            table_name,
            engine,
            if_exists=if_exists,
            index=False,
            method='multi',
            chunksize=1000
        )
        
        print(f"✅ Import réussi: {len(df)} lignes dans {table_name}")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'import: {e}")
        raise

def convert_to_bool(value):
    """
    Convertit différentes représentations en booléen
    """
    if pd.isna(value):
        return None
    
    return str(value).lower().strip() == 'oui'

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

def seed_database():
    """
    Fonction principale de seeding
    """
    print("🌱 Début du seeding...")
    
    create_db_tables()
    
    try:
        import_csv_to_db('data/raw_data.csv', 'clients')
        
        print("✅ Seeding terminé avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur durant le seeding: {e}")

if __name__ == "__main__":
    seed_database()