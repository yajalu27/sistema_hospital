from sqlalchemy.orm import Session
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate

class ClienteRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, cliente_data: ClienteCreate) -> Cliente:
        cliente = Cliente(
            nombre=cliente_data.nombre,
            direccion=cliente_data.direccion,
            telefono=cliente_data.telefono,
            correo=cliente_data.correo
        )
        self.db.add(cliente)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def get(self, cliente_id: int) -> Cliente | None:
        return self.db.query(Cliente).filter(Cliente.id == cliente_id).first()

    def list(self) -> list[Cliente]:
        return self.db.query(Cliente).all()

    def update(self, cliente_id: int, cliente_data: ClienteUpdate) -> Cliente | None:
        cliente = self.get(cliente_id)
        if cliente:
            # Actualizar solo los campos proporcionados
            for key, value in cliente_data.dict(exclude_unset=True).items():
                setattr(cliente, key, value)
            self.db.commit()
            self.db.refresh(cliente)
        return cliente

    def delete(self, cliente_id: int) -> Cliente | None:
        cliente = self.get(cliente_id)
        if cliente:
            self.db.delete(cliente)
            self.db.commit()
        return cliente