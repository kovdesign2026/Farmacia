from typing import List
from service.FacturaService import FacturaService
from service.ClienteService import ClienteService
from service.FarmaceuticoService import FarmaceuticoService
from service.MedicamentoService import MedicamentoService
from model.vo.FacturaVO import FacturaVO
from model.vo.VentaVO import VentaVO


class FacturaController:
    def __init__(self, factura_service: FacturaService,
                 cliente_service: ClienteService,
                 farmaceutico_service: FarmaceuticoService,
                 medicamento_service: MedicamentoService):
        self.factura_service = factura_service
        self.cliente_service = cliente_service
        self.farmaceutico_service = farmaceutico_service
        self.medicamento_service = medicamento_service

    def get_all_facturas(self) -> List[FacturaVO]:
        return self.factura_service.get_all_facturas()

    def get_factura(self, factura_id: int) -> FacturaVO | None:
        return self.factura_service.get_factura(factura_id)

    def insert_factura(self, cliente_id: int, farmaceutico_id: int, medicamento_ids: List[int]) -> bool:
        cliente = self.cliente_service.get_cliente(cliente_id)
        farmaceutico = self.farmaceutico_service.get_farmaceutico(farmaceutico_id)
        
        if not cliente or not farmaceutico:
            return False
        
        ventas = []
        for med_id in medicamento_ids:
            medicamento = self.medicamento_service.get_medicamento(med_id)
            if medicamento:
                ventas.append(VentaVO(None, medicamento))
        
        if not ventas:
            return False
        
        factura = FacturaVO(None, farmaceutico, cliente, ventas)
        self.factura_service.insert_factura(factura)
        return True

    def delete_factura(self, factura_id: int) -> None:
        self.factura_service.delete_factura(factura_id)

    def get_all_clientes(self):
        return self.cliente_service.get_all_clientes()

    def get_all_farmaceuticos(self):
        return self.farmaceutico_service.get_all_farmaceuticos()

    def get_all_medicamentos(self):
        return self.medicamento_service.get_all_medicamentos()
