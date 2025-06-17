from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modèle SQLAlchemy pour une table d'exemple
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)

# Créer les tables dans la base de données (si elles n'existent pas)
# Dans un environnement de production, vous utiliseriez Alembic ou un outil similaire pour les migrations.
Base.metadata.create_all(bind=engine)

router = APIRouter()

# Dépendance pour obtenir la session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.on_event("startup")
async def startup_event():
    logger.info(f"Connecting to database: {DATABASE_URL}")
    # Test de connexion à la base de données au démarrage
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1")) # Simple requête pour tester la connexion
            logger.info("Database connection successful.")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        # Vous pourriez vouloir arrêter l'application ici si la connexion est critique
        # raise HTTPException(status_code=500, detail="Database connection failed")

@router.post("/items/")
async def create_item(name: str, description: str, db: Session = Depends(get_db)):
    db_item = Item(name=name, description=description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    logger.info(f"Created item: {db_item.name}")
    return db_item

@router.get("/items/")
async def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    items = db.query(Item).offset(skip).limit(limit).all()
    logger.info(f"Read {len(items)} items.")
    return items

@router.get("/items/{item_id}")
async def read_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        logger.warning(f"Item with id {item_id} not found.")
        raise HTTPException(status_code=404, detail="Item not found")
    logger.info(f"Read item: {item.name}")
    return item

@router.put("/items/{item_id}")
async def update_item(item_id: int, name: str, description: str, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        logger.warning(f"Item with id {item_id} not found for update.")
        raise HTTPException(status_code=404, detail="Item not found")
    item.name = name
    item.description = description
    db.commit()
    db.refresh(item)
    logger.info(f"Updated item: {item.name}")
    return item

@router.delete("/items/{item_id}")
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        logger.warning(f"Item with id {item_id} not found for deletion.")
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    logger.info(f"Deleted item with id: {item_id}")
    return {"message": f"Item with id {item_id} deleted"}

@router.get("/ping_db/")
async def ping_db(db: Session = Depends(get_db)):
    try:
        # Exécute une simple requête pour vérifier la connexion
        db.execute(text("SELECT 1"))
        logger.info("Database ping successful.")
        return {"status": "Database connection successful"}
    except Exception as e:
        logger.error(f"Database ping failed: {e}")
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")
