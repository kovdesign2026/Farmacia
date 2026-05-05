from typing import List
from service.ClienteService import ClienteService
from model.vo.ClienteVO import ClienteVO


class ClienteController:
    def __init__(self, cliente_service: ClienteService):
        self.cliente_service = cliente_service

    def get_all_clientes(self) -> List[ClienteVO]:
        return self.cliente_service.get_all_clientes()

    def get_cliente(self, cliente_id: int) -> ClienteVO | None:
        return self.cliente_service.get_cliente(cliente_id)

    def insert_cliente(self, nombre: str, dni: str) -> None:
        cliente = ClienteVO(None, nombre, dni)
        self.cliente_service.insert_cliente(cliente)

    def delete_cliente(self, cliente_id: int) -> None:
        self.cliente_service.delete_cliente(cliente_id)
