from api.modules.preprocess import preprocessing, split
from api.modules.evaluate import evaluate_performance
from api.modules.print_draw import print_data, draw_loss
from api.modules.models import create_nn_model, train_model, model_predict
import pandas as pd
import joblib
from os.path import join
from datetime import datetime

# Chargement des datasets
df = pd.read_csv(join('data','preprocessed_new_data.csv'))

# Charger le préprocesseur
preprocessor_loaded = joblib.load(join('api', 'models','preprocessor.pkl'))
# charger le modèle
model_2024_08 = joblib.load(join('api', 'models','model_2025_06_18_10_06.pkl'))

# preprocesser les data
X, y, _ = preprocessing(df)

# split data in train and test dataset
X_train, X_test, y_train, y_test = split(X, y)

# create a new model 
model = create_nn_model(X_train.shape[1])

# entraîner le modèle
model, hist = train_model(model, X_train, y_train, X_val=X_test, y_val=y_test)
draw_loss(hist)

model_name = f"model_{datetime.now().strftime('%Y_%m_%d_%H_%M')}.pkl"
# sauvegarder le modèle
joblib.dump(model, join('api','models',model_name))


#%% predire sur les valeurs de train
y_pred = model_predict(model, X_train)

# mesurer les performances MSE, MAE et R²
perf = evaluate_performance(y_train, y_pred)  

print_data(perf)