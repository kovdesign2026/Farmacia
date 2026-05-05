from typing import List
import pickle
import os

import base64

# Project imports
from model.command.Command import Command

class UndoRedoManager:
    def __init__(self, filename="historial_sesion.txt"):
        self.filename = filename
        self.undo_stack: List[Command] = []
        self.redo_stack: List[Command] = []
        self._load_history()

    def _load_history(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    content = f.read()
                    if content:
                        data_bytes = base64.b64decode(content)
                        data = pickle.loads(data_bytes)
                        self.undo_stack = data.get('undo', [])
                        self.redo_stack = data.get('redo', [])
            except Exception as e:
                print(f"Error loading history from txt: {e}")
                self.undo_stack = []
                self.redo_stack = []

    def _save_history(self):
        try:
            data = {'undo': self.undo_stack, 'redo': self.redo_stack}
            data_bytes = pickle.dumps(data)
            data_b64 = base64.b64encode(data_bytes).decode('utf-8')
            with open(self.filename, 'w') as f:
                f.write(data_b64)
        except Exception as e:
            print(f"Error saving history to txt: {e}")

    def register(self, command: Command) -> None:
        self.undo_stack.append(command)
        self.redo_stack.clear()
        self._save_history()

    def push_redo(self, command: Command) -> None:
        self.redo_stack.append(command)
        self._save_history()

    def push_undo(self, command) -> None:
        self.undo_stack.append(command)
        self._save_history()

    def get_undo(self) -> None | Command:
        if not self.undo_stack:
            return None
        cmd = self.undo_stack.pop()
        self._save_history()
        return cmd
    
    def get_redo(self) -> None | Command:
        if not self.redo_stack:
            return None
        cmd = self.redo_stack.pop()
        self._save_history()
        return cmd
