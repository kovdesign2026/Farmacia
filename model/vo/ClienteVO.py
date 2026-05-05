from dataclasses import dataclass

@dataclass
class ClienteVO:
    cliente_id: int | None
    nombre: str
    dni: str
