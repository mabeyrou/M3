from sklearn.preprocessing import StandardScaler, OneHotEncoder, QuantileTransformer
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pandas as pd

from api.utils.helpers import replace_by_dict

def split(X, y, test_size=0.2, random_state=42):
    '''
    Divises le set de données en sous-ensembles de test et d'entrainement avec la méthode `train_test_split()` de scikitlearn
    args:
    - X : entrées du dataset
    - y : sorties du dataset
    - test_size : proportion du dataset à utiliser pour le test (par défaut 0.2)
    - random_state : pour la reproductibilité des résultats (par défaut 42)
    returns:
    - x_train : entrées du subset d'entrainement
    - y_train : sorties du subset d'entrainement
    - x_test : entrées du subset de test
    - y_test : sorties du subset de test
    '''
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    return X_train, X_test, y_train, y_test

def preprocessing(df):
    '''
    Fonction pour effectuer le prétraitement des données :
    - Imputation des valeurs manquantes.
    - Standardisation des variables numériques.
    - Encodage des variables catégorielles.
    args:
    - df : DataFrame contenant les données à prétraiter
    returns:
    - X_processed : données prétraitées prêtes pour l'entraînement du modèle
    - y : variable cible
    - preprocessor : objet de prétraitement pour une utilisation ultérieure
    '''
    # Suppressions des colonnes sensibles et sans justifiation métier
    cols_to_drop = ['id', 'sexe', 'taille', 'poids', 'smoker']

    for col in cols_to_drop:
        if col not in df.columns:
            print(f"Column '{col}' not found in DataFrame.")
        else:
            print(f"Column '{col}' will be dropped.")
            df = df.drop(columns=col)

    # Catégorisation de l'âge
    bins = [17, 30, 45, 60, 100]
    labels = ['18-29', '30-44', '45-59', '60+']
    df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=True)
    df= df.drop(columns='age')

    # Regroupement des régions
    economy_based_regions = {
    'region_parisienne' : ['Île-de-France'],
    'regions_industrielles': ['Hauts-de-France', 'Grand-Est', 'Bourgogne-Franche-Comté'],
    'regions_tertiaires': ['Bretagne', 'Pays-de-la-Loire', 'Centre-Val-de-Loire', 'Normandie'],
    'regions_touristiques_services': ['Nouvelle-Aquitaine', 'Occitanie', 'Auvergne-Rhône-Alpes', 'PACA', 'Corse'],
    }
    df['region'] = df['region'].apply(lambda x: replace_by_dict(x, economy_based_regions))

    # Transformation de la colonne date_creation_compte en anciennete_mois'
    df['date_creation_compte'] = pd.to_datetime(df['date_creation_compte'], errors='coerce')
    df['anciennete_mois'] = ((pd.Timestamp.now() - df['date_creation_compte']) / pd.Timedelta(days=30)).astype(int)
    df= df.drop(columns='date_creation_compte')

    # Création de colonnes pour les valeurs manquantes
    df['historique_credits_missing_value'] = df['historique_credits'].isna().astype(int)
    df['score_credit_missing_value'] = df['score_credit'].isna().astype(int)
    df['loyer_mensuel_missing_value'] = df['loyer_mensuel'].isna().astype(int)
    df['situation_familiale_missing_value'] = df['situation_familiale'].isna().astype(int)

    numerical_cols = ['revenu_estime_mois', 'risque_personnel', 'loyer_mensuel', 'historique_credits',
                       'score_credit']
    numerical_cols = numerical_cols + ['quotient_caf', 'nb_enfants'] # colonnes ajoutées par les nouvelles données
    categorical_cols = ['age_group', 'sport_licence', 'niveau_etude', 'region', 'situation_familiale',
                        'historique_credits_missing_value', 'score_credit_missing_value', 
                        'loyer_mensuel_missing_value', 'situation_familiale_missing_value']

    # Valeurs aberrantes
    df['loyer_mensuel'] = df['loyer_mensuel'].mask(df['loyer_mensuel'] < 0) # seule colonne avec des valeurs négatives
    
    df.rename(str, axis='columns', inplace=True)  # Assure que les noms de colonnes sont des chaînes de caractères

    num_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='mean')), 
        ('scaler', StandardScaler())
    ])

    cat_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    preprocessor = ColumnTransformer([
        ('num', num_pipeline, numerical_cols),
        ('cat', cat_pipeline, categorical_cols)
    ])

    # Prétraitement
    X = df.drop(columns=['montant_pret'])
    y = df['montant_pret']

    # Fit all transformers, transform the data and concatenate results.
    X_processed = preprocessor.fit_transform(X)
    return X_processed, y, preprocessor

def ethically_loose_preprocessing(df):
    # Suppressions des colonnes sensibles et sans justifiation métier
    cols_to_drop = ['id']
    df = df.drop(columns=cols_to_drop)

    # Création de colonnes pour les valeurs manquantes
    df['historique_credits_missing_value'] = df['historique_credits'].isna().astype(int)
    df['score_credit_missing_value'] = df['score_credit'].isna().astype(int)
    df['loyer_mensuel_missing_value'] = df['loyer_mensuel'].isna().astype(int)
    df['situation_familiale_missing_value'] = df['situation_familiale'].isna().astype(int)
    df['quotient_caf_missing_value'] = df['quotient_caf'].isna().astype(int)
    df['nb_enfants_missing_value'] = df['nb_enfants'].isna().astype(int)

    numerical_cols = ['age', 'taille', 'poids', 'revenu_estime_mois', 'risque_personnel', 'loyer_mensuel', 'historique_credits',
                       'score_credit']
    numerical_cols = numerical_cols + ['quotient_caf', 'nb_enfants'] # colonnes ajoutées par les nouvelles données
    categorical_cols = ['smoker', 'sport_licence', 'niveau_etude', 'region', 'situation_familiale',
                        'historique_credits_missing_value', 'score_credit_missing_value', 
                        'loyer_mensuel_missing_value', 'situation_familiale_missing_value']

    # Valeurs aberrantes
    df['loyer_mensuel'] = df['loyer_mensuel'].mask(df['loyer_mensuel'] < 0) # seule colonne avec des valeurs négatives
    
    df.rename(str, axis='columns', inplace=True)  # Assure que les noms de colonnes sont des chaînes de caractères

    num_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='mean')), 
        ('scaler', StandardScaler())
    ])

    cat_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    preprocessor = ColumnTransformer([
        ('num', num_pipeline, numerical_cols),
        ('cat', cat_pipeline, categorical_cols)
    ])

    # Prétraitement
    X = df.drop(columns=['montant_pret'])
    y = df['montant_pret']

    # Fit all transformers, transform the data and concatenate results.
    X_processed = preprocessor.fit_transform(X)
    return X_processed, y, preprocessor
