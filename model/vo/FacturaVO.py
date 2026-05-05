from dataclasses import dataclass
from typing import List
from model.vo.ClienteVO import ClienteVO
from model.vo.FarmaceuticoVO import FarmaceuticoVO
from model.vo.VentaVO import VentaVO

@dataclass
class FacturaVO:
    factura_id: int | None
    farmaceutico: FarmaceuticoVO
    cliente: ClienteVO
    ventas: List[VentaVO]
