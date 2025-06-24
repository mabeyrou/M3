from sklearn.preprocessing import StandardScaler, OneHotEncoder, QuantileTransformer
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pandas as pd
from loguru import logger

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

def apply_manual_transformations(df, ethically_strict=True):
    """
    Applique les transformations de données manuelles (non-pipeline) à un DataFrame.
    Cette fonction peut être utilisée seule pour préparer les données pour une prédiction.

    args:
    - df: DataFrame d'entrée.
    - ethically_strict: Booléen pour choisir entre le preprocessing strict ou lâche.

    returns:
    - DataFrame avec les transformations manuelles appliquées.
    """
    df = df.copy()

    # Étape 1: Suppression des colonnes
    if ethically_strict:
        cols_to_drop = ['id', 'sexe', 'taille', 'poids', 'smoker']
    else:
        cols_to_drop = ['id']
    
    for col in cols_to_drop:
        if col in df.columns:
            df = df.drop(columns=col)

    # Étape 2: Catégorisation de l'âge (uniquement en mode strict)
    if ethically_strict and 'age' in df.columns:
        bins = [17, 30, 45, 60, 100]
        labels = ['18-29', '30-44', '45-59', '60+']
        df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=True)
        df = df.drop(columns='age')

    # Étape 3: Regroupement des régions
    if 'region' in df.columns:
        economy_based_regions = {
            'region_parisienne' : ['Île-de-France'],
            'regions_industrielles': ['Hauts-de-France', 'Grand-Est', 'Bourgogne-Franche-Comté'],
            'regions_tertiaires': ['Bretagne', 'Pays-de-la-Loire', 'Centre-Val-de-Loire', 'Normandie'],
            'regions_touristiques_services': ['Nouvelle-Aquitaine', 'Occitanie', 'Auvergne-Rhône-Alpes', 'PACA', 'Corse'],
        }
        df['region'] = df['region'].apply(lambda x: replace_by_dict(x, economy_based_regions))

    # Étape 4: Transformation de la date de création en ancienneté
    if 'date_creation_compte' in df.columns:
        df['date_creation_compte'] = pd.to_datetime(df['date_creation_compte'], errors='coerce')
        df['anciennete_mois'] = ((pd.Timestamp.now() - df['date_creation_compte']) / pd.Timedelta(days=30)).astype(int)
        df = df.drop(columns='date_creation_compte')

    # Étape 5: Création des indicateurs de valeurs manquantes
    cols_for_missing_indicator = ['historique_credits', 'score_credit', 'loyer_mensuel', 'situation_familiale', 'quotient_caf', 'nb_enfants']
    for col in cols_for_missing_indicator:
        if col in df.columns:
            df[f'{col}_missing_value'] = df[col].isna().astype(int)

    # Étape 6: Traitement des valeurs aberrantes
    if 'loyer_mensuel' in df.columns:
        df['loyer_mensuel'] = df['loyer_mensuel'].mask(df['loyer_mensuel'] < 0)
    
    # Étape 7: S'assurer que les noms de colonnes sont des chaînes de caractères
    df.rename(str, axis='columns', inplace=True)

    return df

def preprocessing(df):
    '''
    Applique les transformations manuelles puis crée et entraîne un preprocessor
    pour le cas "ethically strict".
    '''
    # Appliquer les transformations manuelles
    df_manual = apply_manual_transformations(df, ethically_strict=True)

    # Définir les listes de colonnes pour la pipeline
    numerical_cols = ['revenu_estime_mois', 'risque_personnel', 'loyer_mensuel', 'historique_credits',
                       'score_credit', 'quotient_caf', 'nb_enfants', 'anciennete_mois']
    categorical_cols = ['age_group', 'sport_licence', 'niveau_etude', 'region', 'situation_familiale',
                        'historique_credits_missing_value', 'score_credit_missing_value', 
                        'loyer_mensuel_missing_value', 'situation_familiale_missing_value',
                        'quotient_caf_missing_value', 'nb_enfants_missing_value']

    # Filtrer les listes pour ne garder que les colonnes présentes
    numerical_cols = [col for col in numerical_cols if col in df_manual.columns]
    categorical_cols = [col for col in categorical_cols if col in df_manual.columns]

    # Définir les pipelines
    num_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='mean')), 
        ('scaler', StandardScaler())
    ])
    cat_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    # Créer le preprocessor
    preprocessor = ColumnTransformer([
        ('num', num_pipeline, numerical_cols),
        ('cat', cat_pipeline, categorical_cols)
    ], remainder='passthrough')

    # Séparer les données et entraîner le preprocessor
    X = df_manual.drop(columns=['montant_pret'])
    y = df_manual['montant_pret']
    X_processed = preprocessor.fit_transform(X)
    
    return X_processed, y, preprocessor

def ethically_loose_preprocessing(df):
    '''
    Applique les transformations manuelles puis crée et entraîne un preprocessor
    pour le cas "ethically loose".
    '''
    # Appliquer les transformations manuelles
    df_manual = apply_manual_transformations(df, ethically_strict=False)

    # Définir les listes de colonnes pour la pipeline
    numerical_cols = ['age', 'taille', 'poids', 'revenu_estime_mois', 'risque_personnel', 'loyer_mensuel', 'historique_credits',
                       'score_credit', 'quotient_caf', 'nb_enfants', 'anciennete_mois']
    categorical_cols = ['smoker', 'sport_licence', 'niveau_etude', 'region', 'situation_familiale',
                        'historique_credits_missing_value', 'score_credit_missing_value', 
                        'loyer_mensuel_missing_value', 'situation_familiale_missing_value',
                        'quotient_caf_missing_value', 'nb_enfants_missing_value']

    # Filtrer les listes pour ne garder que les colonnes présentes
    numerical_cols = [col for col in numerical_cols if col in df_manual.columns]
    categorical_cols = [col for col in categorical_cols if col in df_manual.columns]

    # Définir les pipelines
    num_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='mean')), 
        ('scaler', StandardScaler())
    ])
    cat_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    # Créer le preprocessor
    preprocessor = ColumnTransformer([
        ('num', num_pipeline, numerical_cols),
        ('cat', cat_pipeline, categorical_cols)
    ], remainder='passthrough')

    # Séparer les données et entraîner le preprocessor
    X = df_manual.drop(columns=['montant_pret'])
    y = df_manual['montant_pret']
    X_processed = preprocessor.fit_transform(X)
    
    return X_processed, y, preprocessor
