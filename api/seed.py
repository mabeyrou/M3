import pandas as pd

from api.database import engine, create_db_tables
from api.models import *

def import_csv_to_db(csv_path, table_name, if_exists='append'):
    """
    Importe un CSV directement en base
    
    Args:
        csv_path: Chemin vers le fichier CSV
        table_name: Nom de la table en base
        if_exists: 'append', 'replace', ou 'fail'
    """
    try:
        df = pd.read_csv(csv_path)

        oui_non_cols = get_oui_non_columns(df)
        prohibited_cols = ['nom', 'prenom', 'nationalité_francaise'] # colonnes enfreignant la RGPD

        df = df.assign(**{col: df[col].str.lower().map(convert_to_bool) for col in oui_non_cols})
        df = df.drop(columns=prohibited_cols)
        df['date_creation_compte'] = pd.to_datetime(df['date_creation_compte'], errors='coerce')
        
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

def get_oui_non_columns(df):
    """
    Retourne les colonnes booléennes du DataFrame
    """
    oui_non_columns = []
    for col in df.columns:
        unique_values = df[col].dropna().unique()
        if set(unique_values).issubset({'oui', 'non'}):
            oui_non_columns.append(col)
    return oui_non_columns

def seed_database(csv_path, table):
    """
    Fonction principale de seeding
    """
    print("🌱 Début du seeding...")
    
    create_db_tables()
    
    try:
        import_csv_to_db(csv_path, table, if_exists='append')
        
        print("✅ Seeding terminé avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur durant le seeding: {e}")

if __name__ == "__main__":
    print(f"{' Seeding ':=^60}")
    print("Précisez le chemin vers le fichier CSV :")
    csv_path = input().strip()
    print("Précisez la table de destination :")
    table = input().strip()
    seed_database(csv_path, table)
    print(f"{' Fin du seeding ':=^60}")