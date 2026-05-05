# Project imports
from typing import Callable
from db.Sqlite3Connection import Sqlite3Connection

from model.command.UndoRedoManager import UndoRedoManager

from ui.consoleUtils import log

class HistoryService:

    def __init__(self, 
                 connection_factory: Callable[[], Sqlite3Connection],
                 undo_manager: UndoRedoManager):
        self.connection_factory = connection_factory
        self.undo_manager = undo_manager

    def undo(self) -> None:
        command = self.undo_manager.get_undo()
        if command is None:
            log("There's nothing to undo.")
            return
        
        with self.connection_factory() as connection:
            command.undo(connection)

        self.undo_manager.push_redo(command)
        
    def redo(self) -> None:
        command = self.undo_manager.get_redo()
        if command is None:
            log("There's nothing to redo.")
            return
        
        with self.connection_factory() as connection:
            command.redo(connection)

        self.undo_manager.push_undo(command)
