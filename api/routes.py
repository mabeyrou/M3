from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from loguru import logger

from api.database import get_db
from api.models import Client as ClientModel
from api.schemas import Client as ClientSchema

router = APIRouter(prefix='/api')

@router.get('/')
async def hello_world():
    return {'message': 'Hello, world!'}

@router.post('/clients')
async def create_client(client_data: ClientSchema
, db: Session = Depends(get_db)):
    """Crée un client en base de données"""
    db_client = ClientModel(**client_data.model_dump())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    logger.info(f"Created item: {db_client.name}")
    return db_client

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
            raise HTTPException(status_code=404, detail="Client not found")
        return {'clients': client}
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération de client {str(client_id)}: {str(err)}")

@router.put("/clients/{client_id}")
async def update_client(client_id: int, client_data: ClientSchema, db: Session = Depends(get_db)):
    """Met à jour un client existant dans la base de données"""
    db_client = db.query(ClientModel).filter(ClientModel.id == client_id).first()

    if db_client is None:
        logger.warning(f"Client with id {client_id} not found for update.")
        raise HTTPException(status_code=404, detail="Client not found")
    
    update_data = client_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_client, key, value)
        
    try:
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        logger.info(f"Updated client with id: {db_client.id}") 
        return db_client
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating client with id {client_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error updating client: {str(e)}")

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
