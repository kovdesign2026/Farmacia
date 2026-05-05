from typing import List

# Project imports
from model.command.Command import Command

class UndoRedoManager:
    def __init__(self):
        self.undo_stack: List[Command] = []
        self.redo_stack: List[Command] = []

    def register(self, command: Command) -> None:
        self.undo_stack.append(command)
        self.redo_stack.clear()

    def push_redo(self, command: Command) -> None:
        self.redo_stack.append(command)

    def push_undo(self, command) -> None:
        self.undo_stack.append(command)

    def get_undo(self) -> None | Command:
        if not self.undo_stack:
            return None
        return self.undo_stack.pop()
    
    def get_redo(self) -> None | Command:
        if not self.redo_stack:
            return None
        return self.redo_stack.pop()
