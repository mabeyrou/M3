from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from loguru import logger
import joblib
import pandas as pd
import tensorflow as tf

from api.modules.models import model_predict
from api.database import get_db
from api.models import Client as ClientModel
from api.schemas import Client as ClientSchema
from api.config import DEFAULT_MODEL_PATH, DEFAULT_PREPROCESSOR_PATH
from api.modules.preprocess import apply_manual_transformations

router = APIRouter(prefix='/api')

preprocessor = joblib.load(DEFAULT_PREPROCESSOR_PATH)
model = tf.keras.models.load_model(DEFAULT_MODEL_PATH)

@router.get('/')
async def hello_world():
    return {'message': 'Hello, world!'}

@router.get('/clients')
async def read_clients(db: Session = Depends(get_db)):
    """Récupère tous les clients de la base de données"""
    try:
        clients = db.query(ClientModel).all()
        return {'clients': clients, 'count': len(clients)}
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des clients: {str(err)}")

@router.get('/clients/{client_id}')
async def read_client(client_id: int, db: Session = Depends(get_db)):
    """Récupère un client par son id dans la base de données"""
    try:
        client = db.query(ClientModel).filter(ClientModel.id == client_id).first()
        if not client:
            logger.warning(f'Client with id {client_id} not found.')
            raise HTTPException(status_code=404, detail=f"Client with id {client_id} not found")
        return {'clients': client}
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération de client {str(client_id)}: {str(err)}")

@router.post('/clients')
async def create_client(client_data: ClientSchema
, db: Session = Depends(get_db)):
    """Crée un client en base de données"""
    db_client = ClientModel(**client_data.model_dump())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    logger.info(f"Created item: {db_client.id}")
    return db_client

@router.delete("/clients/{client_id}")
async def delete_client(client_id: int, db: Session = Depends(get_db)):
    """Supprime un client existant dans la base de données"""
    client = db.query(ClientModel).filter(ClientModel.id == client_id).first()
    if client is None:
        logger.warning(f"Client with id {client_id} not found for deletion.")
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(client)
    db.commit()
    logger.info(f"Deleted client with id: {client_id}")
    return {"message": f"Client with id {client_id} deleted"}

@router.post("/predict")
async def predict(client_data: ClientSchema, db: Session = Depends(get_db)):
    """Prédit le risque de crédit pour un client donné"""
    try:
        df = pd.DataFrame([client_data.model_dump()])
        manually_processed_client = apply_manual_transformations(df)
        processed_client = preprocessor.transform(manually_processed_client)
        prediction_array = model_predict(model, processed_client)
        prediction_value = round(prediction_array[0],2)
        logger.info(f'prediction: {prediction_value} avec le client suivant : {client_data}')
        return {'prediction': str(prediction_value)}
    except Exception as e:
        logger.error(f'Prediction processing error for profile {client_data.model_dump()}: {e}')
        detail_message = f"Something went wrong during prediction: {e}"
        raise HTTPException(status_code=500, detail=detail_message)
