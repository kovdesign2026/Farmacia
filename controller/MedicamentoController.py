from typing import List
from service.MedicamentoService import MedicamentoService
from model.vo.MedicamentoVO import MedicamentoVO


class MedicamentoController:
    def __init__(self, medicamento_service: MedicamentoService):
        self.medicamento_service = medicamento_service

    def get_all_medicamentos(self) -> List[MedicamentoVO]:
        return self.medicamento_service.get_all_medicamentos()

    def get_medicamento(self, medicamento_id: int) -> MedicamentoVO | None:
        return self.medicamento_service.get_medicamento(medicamento_id)

    def insert_medicamento(self, nombre: str, dosis: float) -> None:
        medicamento = MedicamentoVO(None, nombre, dosis)
        self.medicamento_service.insert_medicamento(medicamento)

    def delete_medicamento(self, medicamento_id: int) -> None:
        self.medicamento_service.delete_medicamento(medicamento_id)
