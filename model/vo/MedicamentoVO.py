from dataclasses import dataclass

@dataclass
class MedicamentoVO:
    medicamento_id: int | None
    nombre: str
    dosis: float
