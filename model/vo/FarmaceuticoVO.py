from dataclasses import dataclass

@dataclass
class FarmaceuticoVO:
    farmaceutico_id: int | None
    dni: str
    nombre: str
