import pandas as pd
from api.database import engine
import joblib
from os.path import join as join

from api.modules.preprocess import preprocessing

df = pd.read_sql_table(table_name='clients', con=engine)
# df = pd.read_csv(join("data", "raw_data.csv"))

_, _, preprocessor = preprocessing(df)

joblib.dump(preprocessor, join("api", "models", "preprocessor.pkl"))