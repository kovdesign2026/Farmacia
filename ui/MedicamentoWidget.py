from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QTableWidget, QTableWidgetItem, QDialog, QLabel, QLineEdit, 
                           QMessageBox, QDoubleSpinBox, QHeaderView)
from PyQt5.QtCore import Qt
from controller.MedicamentoController import MedicamentoController


class MedicamentoWidget(QWidget):
    def __init__(self, controller: MedicamentoController):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Tabla de medicamentos
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(["ID", "Nombre", "Dosis (mg)"])
        self.tabla.setAlternatingRowColors(True)
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.tabla)
        
        # Botones
        btn_layout = QHBoxLayout()
        btn_agregar = QPushButton("Agregar Medicamento")
        btn_actualizar = QPushButton("Actualizar")
        btn_eliminar = QPushButton("Eliminar")
        btn_eliminar.setObjectName("deleteBtn")
        
        btn_agregar.setMinimumHeight(35)
        btn_actualizar.setMinimumHeight(35)
        btn_eliminar.setMinimumHeight(35)
        
        btn_agregar.clicked.connect(self.agregar_medicamento)
        btn_actualizar.clicked.connect(self.cargar_medicamentos)
        btn_eliminar.clicked.connect(self.eliminar_medicamento)
        
        btn_layout.addWidget(btn_agregar)
        btn_layout.addWidget(btn_actualizar)
        btn_layout.addWidget(btn_eliminar)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        
        self.cargar_medicamentos()

    def cargar_medicamentos(self):
        self.tabla.setRowCount(0)
        medicamentos = self.controller.get_all_medicamentos()
        for med in medicamentos:
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)
            self.tabla.setItem(row, 0, QTableWidgetItem(str(med.medicamento_id)))
            self.tabla.setItem(row, 1, QTableWidgetItem(med.nombre))
            self.tabla.setItem(row, 2, QTableWidgetItem(str(med.dosis)))

    def agregar_medicamento(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Agregar Medicamento")
        dialog.setMinimumWidth(350)
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Nombre:"))
        nombre_input = QLineEdit()
        layout.addWidget(nombre_input)
        
        layout.addWidget(QLabel("Dosis (mg):"))
        dosis_input = QDoubleSpinBox()
        dosis_input.setMinimum(0.1)
        layout.addWidget(dosis_input)
        
        btn_layout = QHBoxLayout()
        btn_guardar = QPushButton("✓ Guardar")
        btn_cancelar = QPushButton("✕ Cancelar")
        btn_guardar.setMinimumHeight(35)
        btn_cancelar.setMinimumHeight(35)
        
        def guardar():
            nombre = nombre_input.text().strip()
            dosis = dosis_input.value()
            if nombre and dosis > 0:
                try:
                    self.controller.insert_medicamento(nombre, dosis)
                    QMessageBox.information(self, "Éxito", "Medicamento agregado correctamente")
                    dialog.accept()
                    self.cargar_medicamentos()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Error al agregar: {str(e)}")
            else:
                QMessageBox.warning(self, "Validación", "Ingrese valores válidos")
        
        btn_guardar.clicked.connect(guardar)
        btn_cancelar.clicked.connect(dialog.reject)
        
        btn_layout.addWidget(btn_guardar)
        btn_layout.addWidget(btn_cancelar)
        layout.addLayout(btn_layout)
        
        dialog.setLayout(layout)
        dialog.exec_()

    def eliminar_medicamento(self):
        fila = self.tabla.currentRow()
        if fila >= 0:
            med_id = int(self.tabla.item(fila, 0).text())
            reply = QMessageBox.question(self, "Confirmar", "¿Eliminar este medicamento?",
                                        QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                try:
                    self.controller.delete_medicamento(med_id)
                    self.cargar_medicamentos()
                    QMessageBox.information(self, "Éxito", "Medicamento eliminado")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Error al eliminar: {str(e)}")
        else:
            QMessageBox.warning(self, "Advertencia", "Seleccione un medicamento para eliminar")
