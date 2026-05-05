from dataclasses import dataclass
from model.vo.MedicamentoVO import MedicamentoVO

@dataclass
class VentaVO:
    venta_id: int | None
    medicamento: MedicamentoVO
