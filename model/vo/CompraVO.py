from dataclasses import dataclass
from model.vo.ProveedorVO import ProveedorVO
from model.vo.MedicamentoVO import MedicamentoVO

@dataclass
class CompraVO:
    compra_id: int | None
    proveedor: ProveedorVO
    medicamento: MedicamentoVO
