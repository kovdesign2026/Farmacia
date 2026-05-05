from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGridLayout)
from PyQt5.QtGui import QFont, QIcon, QColor, QPalette
from PyQt5.QtCore import Qt


class DashboardCard(QFrame):
    def __init__(self, title, value, color, icon_name=None):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title Label
        title_label = QLabel(title)
        title_font = QFont("Inter", 12, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: {color};")
        title_label.setAlignment(Qt.AlignCenter)
        
        # Value Label
        self.value_label = QLabel(str(value))
        value_font = QFont("Inter", 24, QFont.Bold)
        self.value_label.setFont(value_font)
        self.value_label.setStyleSheet("color: #2c3e50;")
        self.value_label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(title_label)
        layout.addSpacing(10)
        layout.addWidget(self.value_label)
        
        self.setLayout(layout)
        
        # Apply specific styling to the card
        self.setStyleSheet(f"""
            DashboardCard {{
                background-color: white;
                border-radius: 10px;
                border-left: 5px solid {color};
            }}
            DashboardCard:hover {{
                background-color: #f8f9fa;
            }}
        """)

    def update_value(self, value):
        self.value_label.setText(str(value))


class DashboardWidget(QWidget):
    def __init__(self, controllers):
        super().__init__()
        self.controllers = controllers
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # Dashboard Title
        title_label = QLabel("Resumen General")
        title_font = QFont("Inter", 24, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2c3e50;")
        main_layout.addWidget(title_label)

        # Cards Layout
        cards_layout = QGridLayout()
        cards_layout.setSpacing(20)

        self.card_clientes = DashboardCard("Total Clientes", 0, "#3498db")
        self.card_medicamentos = DashboardCard("Medicamentos", 0, "#2ecc71")
        self.card_farmaceuticos = DashboardCard("Farmacéuticos", 0, "#9b59b6")
        self.card_proveedores = DashboardCard("Proveedores", 0, "#e67e22")
        self.card_compras = DashboardCard("Compras Registradas", 0, "#e74c3c")
        self.card_facturas = DashboardCard("Facturas Emitidas", 0, "#1abc9c")

        cards_layout.addWidget(self.card_clientes, 0, 0)
        cards_layout.addWidget(self.card_medicamentos, 0, 1)
        cards_layout.addWidget(self.card_farmaceuticos, 0, 2)
        cards_layout.addWidget(self.card_proveedores, 1, 0)
        cards_layout.addWidget(self.card_compras, 1, 1)
        cards_layout.addWidget(self.card_facturas, 1, 2)

        main_layout.addLayout(cards_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)
        self.cargar_datos()

    def cargar_datos(self):
        try:
            num_clientes = len(list(self.controllers["cliente"].get_all_clientes()))
            num_medicamentos = len(list(self.controllers["medicamento"].get_all_medicamentos()))
            num_farmaceuticos = len(list(self.controllers["farmaceutico"].get_all_farmaceuticos()))
            num_proveedores = len(list(self.controllers["proveedor"].get_all_proveedores()))
            num_compras = len(list(self.controllers["compra"].get_all_compras()))
            num_facturas = len(list(self.controllers["factura"].get_all_facturas()))

            self.card_clientes.update_value(num_clientes)
            self.card_medicamentos.update_value(num_medicamentos)
            self.card_farmaceuticos.update_value(num_farmaceuticos)
            self.card_proveedores.update_value(num_proveedores)
            self.card_compras.update_value(num_compras)
            self.card_facturas.update_value(num_facturas)
        except Exception as e:
            print(f"Error cargando dashboard: {e}")
