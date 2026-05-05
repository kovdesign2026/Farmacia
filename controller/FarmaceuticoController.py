from typing import List
from service.FarmaceuticoService import FarmaceuticoService
from model.vo.FarmaceuticoVO import FarmaceuticoVO


class FarmaceuticoController:
    def __init__(self, farmaceutico_service: FarmaceuticoService):
        self.farmaceutico_service = farmaceutico_service

    def get_all_farmaceuticos(self) -> List[FarmaceuticoVO]:
        return self.farmaceutico_service.get_all_farmaceuticos()

    def get_farmaceutico(self, farmaceutico_id: int) -> FarmaceuticoVO | None:
        return self.farmaceutico_service.get_farmaceutico(farmaceutico_id)

    def insert_farmaceutico(self, dni: str, nombre: str) -> None:
        farmaceutico = FarmaceuticoVO(None, dni, nombre)
        self.farmaceutico_service.insert_farmaceutico(farmaceutico)

    def delete_farmaceutico(self, farmaceutico_id: int) -> None:
        self.farmaceutico_service.delete_farmaceutico(farmaceutico_id)
