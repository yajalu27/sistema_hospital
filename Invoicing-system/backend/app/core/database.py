from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm import sessionmaker
import sys
import os
from pathlib import Path

# Get the absolute path to the backend directory
backend_path = str(Path(__file__).parent.parent)
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app.core.config import settings




# Crear el motor de conexión
engine = create_engine(settings.DATABASE_URL)

# Verificar la conexión
try:
    # Intenta conectarse al motor
    with engine.connect() as connection:
        print("Conexión exitosa con la base de datos.")
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
