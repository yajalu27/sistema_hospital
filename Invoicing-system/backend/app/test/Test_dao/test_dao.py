# tests/test_dao.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.core.database import Base
from app.models.producto import Medicamento
from backend.app.models.servicios import AtencionMedica

# Database configuration
DATABASE_URL = "postgresql://postgres:andres@localhost/Testing_sf"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def get_test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()