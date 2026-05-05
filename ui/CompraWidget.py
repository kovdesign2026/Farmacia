from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QTableWidget, QTableWidgetItem, QDialog, QLabel, QSpinBox, QMessageBox, QHeaderView)
from PyQt5.QtCore import Qt
from controller.CompraController import CompraController


class CompraWidget(QWidget):
    def __init__(self, controller: CompraController):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Tabla de compras
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["ID", "Medicamento", "Proveedor", ""])
        self.tabla.setAlternatingRowColors(True)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.tabla)
        
        # Botones
        btn_layout = QHBoxLayout()
        btn_agregar = QPushButton("Registrar Nueva Compra")
        btn_actualizar = QPushButton("Actualizar")
        btn_eliminar = QPushButton("Eliminar")
        btn_eliminar.setObjectName("deleteBtn")
        
        btn_agregar.setMinimumHeight(35)
        btn_actualizar.setMinimumHeight(35)
        btn_eliminar.setMinimumHeight(35)
        
        btn_agregar.clicked.connect(self.agregar_compra)
        btn_actualizar.clicked.connect(self.cargar_compras)
        btn_eliminar.clicked.connect(self.eliminar_compra)
        
        btn_layout.addWidget(btn_agregar)
        btn_layout.addWidget(btn_actualizar)
        btn_layout.addWidget(btn_eliminar)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        
        self.cargar_compras()

    def cargar_compras(self):
        self.tabla.setRowCount(0)
        compras = self.controller.get_all_compras()
        for compra in compras:
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)
            self.tabla.setItem(row, 0, QTableWidgetItem(str(compra.compra_id)))
            self.tabla.setItem(row, 1, QTableWidgetItem(compra.medicamento.nombre))
            self.tabla.setItem(row, 2, QTableWidgetItem(compra.proveedor.razon_social))

    def agregar_compra(self):
        from PyQt5.QtWidgets import QComboBox
        dialog = QDialog(self)
        dialog.setWindowTitle("Registrar Nueva Compra")
        dialog.setMinimumWidth(350)
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Seleccionar Proveedor:"))
        prov_combo = QComboBox()
        proveedores = list(self.controller.get_all_proveedores())
        for p in proveedores:
            prov_combo.addItem(p.razon_social, p.proveedor_id)
        layout.addWidget(prov_combo)
        
        layout.addWidget(QLabel("Seleccionar Medicamento:"))
        med_combo = QComboBox()
        medicamentos = list(self.controller.get_all_medicamentos())
        for m in medicamentos:
            med_combo.addItem(m.nombre, m.medicamento_id)
        layout.addWidget(med_combo)
        
        btn_layout = QHBoxLayout()
        btn_guardar = QPushButton("✓ Guardar")
        btn_cancelar = QPushButton("✕ Cancelar")
        btn_guardar.setMinimumHeight(35)
        btn_cancelar.setMinimumHeight(35)
        
        def guardar():
            if prov_combo.currentData() is None or med_combo.currentData() is None:
                QMessageBox.warning(self, "Advertencia", "Debe seleccionar un proveedor y un medicamento")
                return
                
            prov_id = prov_combo.currentData()
            med_id = med_combo.currentData()
            try:
                if self.controller.insert_compra(prov_id, med_id):
                    QMessageBox.information(self, "Éxito", "Compra registrada correctamente")
                    dialog.accept()
                    self.cargar_compras()
                else:
                    QMessageBox.critical(self, "Error", "Proveedor o Medicamento no encontrado")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al registrar: {str(e)}")
        
        btn_guardar.clicked.connect(guardar)
        btn_cancelar.clicked.connect(dialog.reject)
        
        btn_layout.addWidget(btn_guardar)
        btn_layout.addWidget(btn_cancelar)
        layout.addLayout(btn_layout)
        
        dialog.setLayout(layout)
        dialog.exec_()

    def eliminar_compra(self):
        fila = self.tabla.currentRow()
        if fila >= 0:
            compra_id = int(self.tabla.item(fila, 0).text())
            reply = QMessageBox.question(self, "Confirmar", "¿Eliminar esta compra?",
                                        QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                try:
                    self.controller.delete_compra(compra_id)
                    self.cargar_compras()
                    QMessageBox.information(self, "Éxito", "Compra eliminada")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Error al eliminar: {str(e)}")
        else:
            QMessageBox.warning(self, "Advertencia", "Seleccione una compra para eliminar")
