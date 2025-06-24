import tensorflow as tf
import pandas as pd
import mlflow
from mlflow.models import infer_signature
from os.path import join


from api.modules.preprocess import preprocessing, split, ethically_loose_preprocessing
from api.modules.evaluate import evaluate_performance
from api.modules.models import train_model, model_predict, create_nn_model, create_nn_model_based_on
from api.database import engine


df = pd.read_sql_table(table_name='clients', con=engine)

mlflow.set_experiment("Training loan prediction model with data from brief 0")
mlflow.autolog()

"""
Ethically strict preprocessing:
"""
with mlflow.start_run():
    X, y, _ = preprocessing(df.tail(10000))

    X_train, X_test, y_train, y_test = split(X, y)

    # Charger le modèle 1 et transférer les poids compatibles
    old_ethically_strict_model = tf.keras.models.load_model(join('.', 'models', 'ethically_strict_model.keras'))

    # Charger le modèle 1 et transférer les poids compatibles
    new_ethically_strict_model = create_nn_model_based_on(
        base_model=old_ethically_strict_model, input_dim=X_train.shape[1])


    new_ethically_strict_model, history_ethically_strict = train_model(
        new_ethically_strict_model, X_train, y_train, X_val=X_test, y_val=y_test)
    
    y_pred = model_predict(new_ethically_strict_model, X_train)

    perf = evaluate_performance(y_train, y_pred)  

    mlflow.log_metric("R²", perf['R²'])
    mlflow.log_metric("MSE", perf['MSE'])
    mlflow.log_metric("MAE", perf['MAE'])

    mlflow.set_tag("Data Processing Info", "NEW ethically strict preprocessing")
    mlflow.set_tag("Training Info", "30 epochs")

    signature = infer_signature(X_train, model_predict(new_ethically_strict_model, X_train))

    model_info = mlflow.sklearn.log_model(
        sk_model=new_ethically_strict_model,
        artifact_path="iris_model",
        signature=signature,
        input_example=X_train,
        registered_model_name="new_loan-prediction-ethical-model",
    )
    
    # Sauvegarde du modèle complet
    new_ethically_strict_model.save(join('.', 'models', 'new-ethically_strict_model.keras'))

"""
Ethically loose preprocessing:
"""
with mlflow.start_run():
    X, y, _ = ethically_loose_preprocessing(df.tail(10000))

    X_train, X_test, y_train, y_test = split(X, y)

    # Charger le modèle 1 et transférer les poids compatibles
    old_ethically_loose_model = tf.keras.models.load_model(join('.', 'models', 'ethically_loose_model.keras'))

    # Charger le modèle 1 et transférer les poids compatibles
    new_ethically_loose_model = create_nn_model_based_on(
        base_model=old_ethically_loose_model, input_dim=X_train.shape[1])


    new_ethically_loose_model, history_ethically_strict = train_model(
        new_ethically_loose_model, X_train, y_train, X_val=X_test, y_val=y_test)
    
    y_pred = model_predict(new_ethically_loose_model, X_train)

    perf = evaluate_performance(y_train, y_pred)  

    mlflow.log_metric("R²", perf['R²'])
    mlflow.log_metric("MSE", perf['MSE'])
    mlflow.log_metric("MAE", perf['MAE'])

    mlflow.set_tag("Data Processing Info", "NEW ethically loose preprocessing")
    mlflow.set_tag("Training Info", "30 epochs")

    signature = infer_signature(X_train, model_predict(new_ethically_loose_model, X_train))

    model_info = mlflow.sklearn.log_model(
        sk_model=new_ethically_loose_model,
        artifact_path="iris_model",
        signature=signature,
        input_example=X_train,
        registered_model_name="new-loan-prediction-ethical-model",
    )
    
    # Sauvegarde du modèle complet
    new_ethically_loose_model.save(join('.', 'models', 'new_ethically_loose_model.keras'))