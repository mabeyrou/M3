import joblib
import pandas as pd
import mlflow
from mlflow.models import infer_signature
from os.path import join as join
from datetime import datetime

from api.modules.preprocess import preprocessing, split, ethically_loose_preprocessing
from api.modules.evaluate import evaluate_performance
from api.modules.models import train_model, model_predict, create_nn_model
from api.modules.print_draw import draw_loss
from api.database import engine


df = pd.read_sql_table(table_name='clients', con=engine)

ethically_strict_preprocessor_loaded = joblib.load(join('.', 'models','ethically_strict_preprocessor.pkl'))
ethically_loose_preprocessor_loaded = joblib.load(join('.', 'models','ethically_loose_preprocessor.pkl'))

mlflow.set_experiment("Training loan prediction model with data from brief 0")
mlflow.autolog()

with mlflow.start_run():
    X, y, _ = preprocessing(df)

    X_train, X_test, y_train, y_test = split(X, y)

    model = create_nn_model(X_train.shape[1])
    model, _ = train_model(model, X_train, y_train, X_val=X_test, y_val=y_test, epochs=30)
    y_pred = model_predict(model, X_test)
    perf = evaluate_performance(y_test, y_pred)  

    mlflow.log_metric("R²", perf['R²'])
    mlflow.log_metric("MSE", perf['MSE'])
    mlflow.log_metric("MAE", perf['MAE'])

    mlflow.set_tag("Data Processing Info", "Ethically strict preprocessing")
    mlflow.set_tag("Training Info", "30 epochs")

    signature = infer_signature(X_train, model_predict(model, X_train))

    model_info = mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="iris_model",
        signature=signature,
        input_example=X_train,
        registered_model_name="loan-prediction-ethical-model",
    )
    
    # sauvegarder le modèle
    model_name = f"model_ethically_strict_{datetime.now().strftime('%Y_%m_%d_%H_%M')}.keras"
    model.save(join('.', 'models', model_name))

with mlflow.start_run():
    X, y, _ = ethically_loose_preprocessing(df)

    X_train, X_test, y_train, y_test = split(X, y)

    model = create_nn_model(X_train.shape[1])
    model, _ = train_model(model, X_train, y_train, X_val=X_test, y_val=y_test, epochs=30)
    y_pred = model_predict(model, X_test)
    perf = evaluate_performance(y_test, y_pred)  

    mlflow.log_metric("R²", perf['R²'])
    mlflow.log_metric("MSE", perf['MSE'])
    mlflow.log_metric("MAE", perf['MAE'])

    mlflow.set_tag("Data Processing Info", "Ethically loose preprocessing")
    mlflow.set_tag("Training Info", "30 epochs")

    signature = infer_signature(X_train, model_predict(model, X_train))

    model_info = mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="iris_model",
        signature=signature,
        input_example=X_train,
        registered_model_name="loan-prediction-ethical-model",
    )
    
    # sauvegarder le modèle
    model_name = f"model_ethically_loose_{datetime.now().strftime('%Y_%m_%d_%H_%M')}.keras"
    model.save(join('.', 'models', model_name))
