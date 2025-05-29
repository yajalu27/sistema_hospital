from sqlalchemy.orm import Session
from app.repositories.cliente_repository import ClienteRepository
from app.schemas.cliente import ClienteCreate, ClienteUpdate
from app.models.cliente import Cliente

class ClienteService:
    def __init__(self, db: Session):
        self.repo = ClienteRepository(db)

    def create_cliente(self, cliente_data: ClienteCreate) -> Cliente:
        return self.repo.create(cliente_data)

    def get_cliente(self, cliente_id: int) -> Cliente | None:
        return self.repo.get(cliente_id)

    def list_clientes(self) -> list[Cliente]:
        return self.repo.list()

    def update_cliente(self, cliente_id: int, cliente_data: ClienteUpdate) -> Cliente | None:
        return self.repo.update(cliente_id, cliente_data)

    def delete_cliente(self, cliente_id: int) -> Cliente | None:
        return self.repo.delete(cliente_id)
    

    