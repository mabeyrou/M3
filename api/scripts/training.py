import joblib
import pandas as pd
import mlflow
from mlflow.models import infer_signature
from os.path import join as join

from api.modules.preprocess import preprocessing, split
from api.modules.evaluate import evaluate_performance
from api.modules.models import train_model, model_predict, create_nn_model
from api.database import engine

df = pd.read_sql_table(table_name='clients', con=engine)

old_model = joblib.load(join('models','model_2024_08.pkl'))

mlflow.set_experiment("Training loan prediction model with data from brief 0")
mlflow.autolog()

with mlflow.start_run():
    retraining_data = df
    X, y, _ = preprocessing(retraining_data)

    X_train, X_test, y_train, y_test = split(X, y)

    retrained_model, _ = train_model(old_model, X_train, y_train, X_val=X_test, y_val=y_test, epochs=50)
    y_pred = model_predict(old_model, X_test)
    perf = evaluate_performance(y_test, y_pred)  

    mlflow.log_metric("R²", perf['R²'])

    mlflow.set_tag("Data Processing Info", "Strict ethical preprocessing")
    mlflow.set_tag("Training Info", "50 epochs")

    signature = infer_signature(X_train, model_predict(retrained_model, X_train))

    model_info = mlflow.sklearn.log_model(
        sk_model=retrained_model,
        artifact_path="iris_model",
        signature=signature,
        input_example=X_train,
        registered_model_name="loan-prediction-ethical-model",
    )
