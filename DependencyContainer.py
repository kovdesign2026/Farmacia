from db.Sqlite3Connection import Sqlite3Connection
from service.ClienteService import ClienteService
from service.MedicamentoService import MedicamentoService
from service.FarmaceuticoService import FarmaceuticoService
from service.ProveedorService import ProveedorService
from service.CompraService import CompraService
from service.FacturaService import FacturaService
from service.HistoryService import HistoryService

from controller.ClienteController import ClienteController
from controller.MedicamentoController import MedicamentoController
from controller.FarmaceuticoController import FarmaceuticoController
from controller.ProveedorController import ProveedorController
from controller.CompraController import CompraController
from controller.FacturaController import FacturaController
from controller.HistoryController import HistoryController

from model.command.UndoRedoManager import UndoRedoManager

class DependencyContainer:
    def __init__(self):
        self.connection_factory = lambda: Sqlite3Connection("db/farmacia.db")
        self.undo_manager = UndoRedoManager()
        
        # Init Services
        self.services = {
            "cliente": ClienteService(self.connection_factory, self.undo_manager),
            "medicamento": MedicamentoService(self.connection_factory, self.undo_manager),
            "farmaceutico": FarmaceuticoService(self.connection_factory, self.undo_manager),
            "proveedor": ProveedorService(self.connection_factory, self.undo_manager),
            "compra": CompraService(self.connection_factory, self.undo_manager),
            "factura": FacturaService(self.connection_factory, self.undo_manager),
            "history": HistoryService(self.connection_factory, self.undo_manager),
        }
        
        # Init Controllers
        self.controllers = {
            "cliente": ClienteController(self.services["cliente"]),
            "medicamento": MedicamentoController(self.services["medicamento"]),
            "farmaceutico": FarmaceuticoController(self.services["farmaceutico"]),
            "proveedor": ProveedorController(self.services["proveedor"]),
            "compra": CompraController(
                self.services["compra"],
                self.services["proveedor"],
                self.services["medicamento"]
            ),
            "factura": FacturaController(
                self.services["factura"],
                self.services["cliente"],
                self.services["farmaceutico"],
                self.services["medicamento"]
            ),
            "history": HistoryController(self.services["history"]),
        }
