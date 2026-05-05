from service.HistoryService import HistoryService

class HistoryController:

    def __init__(self, history_service: HistoryService):
        self.history_service = history_service

    def undo(self) -> None:
        self.history_service.undo()

    def redo(self) -> None:
        self.history_service.redo()
