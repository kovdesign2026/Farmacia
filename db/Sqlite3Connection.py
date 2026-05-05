import sqlite3
from sqlite3 import Connection
from typing import Any

# Project imports
from ui.consoleUtils import log

# Context for database connection gestor
class Sqlite3Connection:

    def __init__(self, db_path: str='./'):
        self.db_path = db_path
        self.connection: Connection | None = None

    # Se ejecuta al usar el contexto "with"
    def __enter__(self) -> 'Sqlite3Connection':
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row

        log("Conexión abierta...")

        # Retornamos self para que el gestor de contexto funcione correctamente
        return self
    
    # Se ejecuta al salir del contexto o cuando ocurre una excepci n
    def __exit__(self, exec_type, exec, traceback) -> bool | None:
        if self.connection is None:
            return 
        
        if exec_type is None:
            log("Guardando cambios (Commit)...")

            self.connection.commit()

        # Si ocurre una excepci n
        else:
            log("Deshaciendo cambios por error (Rollback)...")
            log(f"Tipo de Excepción -> {exec_type}")
            log(f"Excepción -> {exec}")
            self.connection.rollback()

        self.connection.close()

        return False
    
    def __getattr__(self, name) -> Any:
        if self.connection is None:
            raise AttributeError("Connection not initialized")
        return getattr(self.connection, name)
