import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input
import pandas as pd
import mlflow
from mlflow.models import infer_signature
from os.path import join as join
from sklearn.metrics import r2_score


from api.modules.preprocess import preprocessing, split, ethically_loose_preprocessing
from api.modules.evaluate import evaluate_performance
from api.modules.models import train_model, model_predict, create_nn_model
from api.modules.print_draw import draw_loss
from api.database import engine


df = pd.read_sql_table(table_name='clients', con=engine)

mlflow.set_experiment("Training loan prediction model with data from brief 0")
mlflow.autolog()
"""
Ethically strict preprocessing:
"""
with mlflow.start_run():
    X, y, _ = preprocessing(df.head(10000))

    X_train, X_test, y_train, y_test = split(X, y)

    ethically_strict_model = create_nn_model(input_dim=X_train.shape[1])

    ethically_strict_model, history_ethically_strict = train_model(
        ethically_strict_model, X_train, y_train, X_val=X_test, y_val=y_test)
    
    y_pred = model_predict(ethically_strict_model, X_train)

    perf = evaluate_performance(y_train, y_pred)  

    mlflow.log_metric("R²", perf['R²'])
    mlflow.log_metric("MSE", perf['MSE'])
    mlflow.log_metric("MAE", perf['MAE'])

    mlflow.set_tag("Data Processing Info", "Ethically strict preprocessing")
    mlflow.set_tag("Training Info", "30 epochs")

    signature = infer_signature(X_train, model_predict(ethically_strict_model, X_train))

    model_info = mlflow.sklearn.log_model(
        sk_model=ethically_strict_model,
        artifact_path="iris_model",
        signature=signature,
        input_example=X_train,
        registered_model_name="loan-prediction-ethical-model",
    )
    
    # Sauvegarde du modèle complet
    ethically_strict_model.save(join('.', 'models', 'ethically_strict_model.keras'))

"""
Ethically loose preprocessing:
"""
with mlflow.start_run():
    X, y, _ = ethically_loose_preprocessing(df.head(10000))

    X_train, X_test, y_train, y_test = split(X, y)

    ethically_loose_model = create_nn_model(input_dim=X_train.shape[1])

    ethically_loose_model, history_ethically_loose = train_model(
        ethically_loose_model, X_train, y_train, X_val=X_test, y_val=y_test)
    
    y_pred = model_predict(ethically_loose_model, X_train)

    perf = evaluate_performance(y_train, y_pred)  

    mlflow.log_metric("R²", perf['R²'])
    mlflow.log_metric("MSE", perf['MSE'])
    mlflow.log_metric("MAE", perf['MAE'])

    mlflow.set_tag("Data Processing Info", "Ethically strict preprocessing")
    mlflow.set_tag("Training Info", "30 epochs")

    signature = infer_signature(X_train, model_predict(ethically_loose_model, X_train))

    model_info = mlflow.sklearn.log_model(
        sk_model=ethically_loose_model,
        artifact_path="iris_model",
        signature=signature,
        input_example=X_train,
        registered_model_name="loan-prediction-ethical-model",
    )
    
    # Sauvegarde du modèle complet
    ethically_loose_model.save(join('.', 'models', 'ethically_loose_model.keras'))