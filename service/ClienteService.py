from typing import List, Callable
from db.Sqlite3Connection import Sqlite3Connection
from model.vo.ClienteVO import ClienteVO
from model.dao.ClienteDAO import ClienteDAO

from model.command.UndoRedoManager import UndoRedoManager
from model.command.ClienteCommand import InsertClienteCommand, DeleteClienteCommand

class ClienteService:
    def __init__(self, connection_factory: Callable[[], Sqlite3Connection], undo_manager: UndoRedoManager = None):
        self.connection_factory = connection_factory
        self.undo_manager = undo_manager

    def get_all_clientes(self) -> List[ClienteVO]:
        return ClienteDAO.get_all_clientes()
    
    def get_cliente(self, cliente_id: int) -> ClienteVO | None:
        return ClienteDAO.get_cliente(cliente_id)

    def insert_cliente(self, cliente: ClienteVO):
        with self.connection_factory() as connection:
            result = ClienteDAO.insert_cliente(connection, cliente)
            if result:
                cliente.cliente_id = result
                if self.undo_manager:
                    self.undo_manager.register(InsertClienteCommand(cliente))
            return result

    def delete_cliente(self, cliente_id: int) -> None:
        vo = self.get_cliente(cliente_id)
        if vo:
            ClienteDAO.delete_cliente(cliente_id)
            if self.undo_manager:
                self.undo_manager.register(DeleteClienteCommand(vo))
