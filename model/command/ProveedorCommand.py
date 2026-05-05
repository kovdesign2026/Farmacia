from model.command.Command import Command
from model.vo.ProveedorVO import ProveedorVO
from model.dao.ProveedorDAO import ProveedorDAO
from db.Sqlite3Connection import Sqlite3Connection


class InsertProveedorCommand(Command):
    def __init__(self, proveedor: ProveedorVO):
        self.proveedor = proveedor

    def undo(self, connection: Sqlite3Connection):
        if self.proveedor.proveedor_id:
            ProveedorDAO.delete_proveedor(self.proveedor.proveedor_id)

    def redo(self, connection: Sqlite3Connection):
        if self.proveedor.proveedor_id:
            ProveedorDAO.reinsert_proveedor(connection, self.proveedor)
        else:
            result = ProveedorDAO.insert_proveedor(connection, self.proveedor)
            if result:
                self.proveedor.proveedor_id = result


class DeleteProveedorCommand(Command):
    def __init__(self, proveedor: ProveedorVO):
        self.proveedor = proveedor

    def undo(self, connection: Sqlite3Connection):
        ProveedorDAO.reinsert_proveedor(connection, self.proveedor)

    def redo(self, connection: Sqlite3Connection):
        ProveedorDAO.delete_proveedor(self.proveedor.proveedor_id)
