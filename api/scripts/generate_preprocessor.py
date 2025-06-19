import pandas as pd
from api.database import engine
import joblib
from os.path import join as join

from api.modules.preprocess import preprocessing

df = pd.read_sql_table(
    table_name='clients',
    con=engine,
    parse_dates=['date_creation_compte']  
)

_, _, preprocessor = preprocessing(df)

joblib.dump(preprocessor, join(".", "models", "preprocessor.pkl"))