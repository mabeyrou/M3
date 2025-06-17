from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from loguru import logger

from .database import get_db
from .models import Client

router = APIRouter(prefix='/api')

@router.get('/')
async def hello_world():
    return {'message': 'Hello, world!'}

@router.post('/clients')
async def create_client(client: Client, db: Session = Depends(get_db)):
    """Crée un client en base de données"""
    db_client = Client(name=name, description=description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    logger.info(f"Created item: {db_item.name}")
    return db_item
    try:
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            logger.warning(f'Client with id {client_id} not found.')
            raise HTTPException(status_code=404, detail="Client not found")
        return {'client': client}
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération de client {str(client_id)}: {str(err)}")

@router.get('/clients')
async def read_clients(db: Session = Depends(get_db)):
    """Récupère tous les clients de la base de données"""
    try:
        clients = db.query(Client).all()
        return {'clients': clients, 'count': len(clients)}
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des clients: {str(err)}")

@router.get('/clients/{client_id}')
async def read_client(client_id: int, db: Session = Depends(get_db)):
    """Récupère un client par son id dans la base de données"""
    try:
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            logger.warning(f'Client with id {client_id} not found.')
            raise HTTPException(status_code=404, detail="Client not found")
        return {'clients': client}
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération de client {str(client_id)}: {str(err)}")
