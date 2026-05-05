from model.command.Command import Command
from model.vo.CompraVO import CompraVO
from model.dao.CompraDAO import CompraDAO
from db.Sqlite3Connection import Sqlite3Connection


class InsertCompraCommand(Command):
    def __init__(self, compra: CompraVO):
        self.compra = compra

    def undo(self, connection: Sqlite3Connection):
        if self.compra.compra_id:
            CompraDAO.delete_compra(self.compra.compra_id)

    def redo(self, connection: Sqlite3Connection):
        if self.compra.compra_id:
            CompraDAO.reinsert_compra(connection, self.compra)
        else:
            result = CompraDAO.insert_compra(connection, self.compra)
            if result:
                self.compra.compra_id = result


class DeleteCompraCommand(Command):
    def __init__(self, compra: CompraVO):
        self.compra = compra

    def undo(self, connection: Sqlite3Connection):
        CompraDAO.reinsert_compra(connection, self.compra)

    def redo(self, connection: Sqlite3Connection):
        CompraDAO.delete_compra(self.compra.compra_id)
