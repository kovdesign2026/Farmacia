from abc import ABC, abstractmethod
from db.Sqlite3Connection import Sqlite3Connection

class Command(ABC):
    @abstractmethod
    def undo(self, connection: Sqlite3Connection):
        pass

    @abstractmethod
    def redo(self, connection: Sqlite3Connection):
        pass