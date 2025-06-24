import pandas as pd
from api.database import engine
import joblib
from os.path import join as join

from api.modules.preprocess import preprocessing, ethically_loose_preprocessing

df = pd.read_sql_table(
    table_name='clients',
    con=engine,
    parse_dates=['date_creation_compte'],
)

_, _, preprocessor = preprocessing(df)
_, _, ethically_loose_preprocessor = ethically_loose_preprocessing(df)

joblib.dump(preprocessor, join(".", "models", "new_ethically_strict_preprocessor.pkl"))
joblib.dump(ethically_loose_preprocessor, join(".", "models", "new_ethically_loose_preprocessor.pkl"))