from typing import List
from service.CompraService import CompraService
from service.ProveedorService import ProveedorService
from service.MedicamentoService import MedicamentoService
from model.vo.CompraVO import CompraVO


class CompraController:
    def __init__(self, compra_service: CompraService, 
                 proveedor_service: ProveedorService,
                 medicamento_service: MedicamentoService):
        self.compra_service = compra_service
        self.proveedor_service = proveedor_service
        self.medicamento_service = medicamento_service

    def get_all_compras(self) -> List[CompraVO]:
        return self.compra_service.get_all_compras()

    def get_compra(self, compra_id: int) -> CompraVO | None:
        return self.compra_service.get_compra(compra_id)

    def insert_compra(self, proveedor_id: int, medicamento_id: int) -> bool:
        proveedor = self.proveedor_service.get_proveedor(proveedor_id)
        medicamento = self.medicamento_service.get_medicamento(medicamento_id)
        
        if not proveedor or not medicamento:
            return False
        
        compra = CompraVO(None, proveedor, medicamento)
        self.compra_service.insert_compra(compra)
        return True

    def delete_compra(self, compra_id: int) -> None:
        self.compra_service.delete_compra(compra_id)

    def get_all_proveedores(self):
        return self.proveedor_service.get_all_proveedores()

    def get_all_medicamentos(self):
        return self.medicamento_service.get_all_medicamentos()
