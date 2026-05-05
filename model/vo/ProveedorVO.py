from dataclasses import dataclass

@dataclass
class ProveedorVO:
    proveedor_id: int | None
    razon_social: str
    nit: str
