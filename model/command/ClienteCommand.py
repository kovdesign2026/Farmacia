from model.command.Command import Command
from model.vo.ClienteVO import ClienteVO
from model.dao.ClienteDAO import ClienteDAO
from db.Sqlite3Connection import Sqlite3Connection


class InsertClienteCommand(Command):
    def __init__(self, cliente: ClienteVO):
        self.cliente = cliente

    def undo(self, connection: Sqlite3Connection):
        if self.cliente.cliente_id:
            ClienteDAO.delete_cliente(self.cliente.cliente_id)

    def redo(self, connection: Sqlite3Connection):
        # Si ya existe un ID, reinsertar con ese ID
        if self.cliente.cliente_id:
            ClienteDAO.reinsert_cliente(connection, self.cliente)
        else:
            # Inserción inicial (no debería ocurrir en este flujo)
            result = ClienteDAO.insert_cliente(connection, self.cliente)
            if result:
                self.cliente.cliente_id = result


class DeleteClienteCommand(Command):
    def __init__(self, cliente: ClienteVO):
        self.cliente = cliente

    def undo(self, connection: Sqlite3Connection):
        ClienteDAO.reinsert_cliente(connection, self.cliente)

    def redo(self, connection: Sqlite3Connection):
        ClienteDAO.delete_cliente(self.cliente.cliente_id)
