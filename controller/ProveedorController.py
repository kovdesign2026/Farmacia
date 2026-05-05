from typing import List
from service.ProveedorService import ProveedorService
from model.vo.ProveedorVO import ProveedorVO


class ProveedorController:
    def __init__(self, proveedor_service: ProveedorService):
        self.proveedor_service = proveedor_service

    def get_all_proveedores(self) -> List[ProveedorVO]:
        return self.proveedor_service.get_all_proveedores()

    def get_proveedor(self, proveedor_id: int) -> ProveedorVO | None:
        return self.proveedor_service.get_proveedor(proveedor_id)

    def insert_proveedor(self, razon_social: str, nit: str) -> None:
        proveedor = ProveedorVO(None, razon_social, nit)
        self.proveedor_service.insert_proveedor(proveedor)

    def delete_proveedor(self, proveedor_id: int) -> None:
        self.proveedor_service.delete_proveedor(proveedor_id)
