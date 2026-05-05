from PyQt5.QtWidgets import (QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QPushButton)
from PyQt5.QtGui import QIcon, QFont, QColor
from PyQt5.QtCore import Qt

from ui.ClienteWidget import ClienteWidget
from ui.MedicamentoWidget import MedicamentoWidget
from ui.FarmaceuticoWidget import FarmaceuticoWidget
from ui.ProveedorWidget import ProveedorWidget
from ui.CompraWidget import CompraWidget
from ui.FacturaWidget import FacturaWidget
from ui.DashboardWidget import DashboardWidget


class MainWindow(QMainWindow):
    def __init__(self, controllers):
        super().__init__()
        self.controllers = controllers
        self.history_controller = self.controllers["history"]
        self.init_ui()
        self.apply_styles()



    def init_ui(self):
        self.setWindowTitle("Sistema Integral de Farmacia")
        self.setGeometry(100, 100, 1200, 700)

        # Widget central
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Toolbar con botones Undo/Redo
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setContentsMargins(10, 10, 10, 10)
        
        btn_undo = QPushButton("Deshacer")
        btn_redo = QPushButton("Rehacer")
        
        btn_undo.setMaximumWidth(120)
        btn_redo.setMaximumWidth(120)
        btn_undo.setCursor(Qt.PointingHandCursor)
        btn_redo.setCursor(Qt.PointingHandCursor)
        
        btn_undo.clicked.connect(self.undo_action)
        btn_redo.clicked.connect(self.redo_action)
        
        toolbar_layout.addWidget(btn_undo)
        toolbar_layout.addWidget(btn_redo)
        toolbar_layout.addStretch()
        
        main_layout.addLayout(toolbar_layout)

        # Tabs
        tabs = QTabWidget()
        tabs.setDocumentMode(True)
        tabs.tabBar().setExpanding(True)

        # Crear widgets y guardar referencias
        self.dashboard_widget = DashboardWidget(self.controllers)
        self.cliente_widget = ClienteWidget(self.controllers["cliente"])
        self.medicamento_widget = MedicamentoWidget(self.controllers["medicamento"])
        self.farmaceutico_widget = FarmaceuticoWidget(self.controllers["farmaceutico"])
        self.proveedor_widget = ProveedorWidget(self.controllers["proveedor"])
        self.compra_widget = CompraWidget(self.controllers["compra"])
        self.factura_widget = FacturaWidget(self.controllers["factura"])

        # Agregar cada widget como una pestaña
        tabs.addTab(self.dashboard_widget, "Dashboard")
        tabs.addTab(self.cliente_widget, "Clientes")
        tabs.addTab(self.medicamento_widget, "Medicamentos")
        tabs.addTab(self.farmaceutico_widget, "Farmacéuticos")
        tabs.addTab(self.proveedor_widget, "Proveedores")
        tabs.addTab(self.compra_widget, "Compras")
        tabs.addTab(self.factura_widget, "Facturas")

        main_layout.addWidget(tabs)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def undo_action(self):
        self.history_controller.undo()
        self.refresh_all_widgets()

    def redo_action(self):
        self.history_controller.redo()
        self.refresh_all_widgets()

    def refresh_all_widgets(self):
        """Actualiza todos los widgets después de un undo/redo"""
        self.dashboard_widget.cargar_datos()
        self.cliente_widget.cargar_clientes()
        self.medicamento_widget.cargar_medicamentos()
        self.farmaceutico_widget.cargar_farmaceuticos()
        self.proveedor_widget.cargar_proveedores()
        self.compra_widget.cargar_compras()
        self.factura_widget.cargar_facturas()

    def apply_styles(self):
        stylesheet = """
        QMainWindow {
            background-color: #f8f9fa;
        }
        
        QTabWidget::pane {
            border: none;
            background-color: #ffffff;
            border-radius: 8px;
            margin: 10px;
        }
        
        QTabBar::tab {
            background-color: transparent;
            color: #6c757d;
            padding: 12px 20px;
            margin: 5px;
            font-size: 14px;
            font-weight: 600;
            border-radius: 6px;
        }
        
        QTabBar::tab:selected {
            background-color: #2c3e50;
            color: #ffffff;
        }
        
        QTabBar::tab:hover:!selected {
            background-color: #e9ecef;
            color: #495057;
        }
        
        QPushButton {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            font-weight: bold;
            font-size: 13px;
        }
        
        QPushButton:hover {
            background-color: #2980b9;
        }
        
        QPushButton:pressed {
            background-color: #1c5980;
        }
        
        QPushButton#deleteBtn {
            background-color: #e74c3c;
        }
        
        QPushButton#deleteBtn:hover {
            background-color: #c0392b;
        }
        
        QTableWidget {
            background-color: #ffffff;
            alternate-background-color: #f8f9fa;
            gridline-color: #ecf0f1;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            font-size: 13px;
        }
        
        QTableWidget::item {
            padding: 8px;
            border-bottom: 1px solid #ecf0f1;
            color: #2c3e50;
        }
        
        QHeaderView::section {
            background-color: #2c3e50;
            color: #ffffff;
            padding: 10px;
            border: none;
            font-weight: bold;
            font-size: 13px;
        }
        
        QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
            padding: 8px 12px;
            border: 1px solid #ced4da;
            border-radius: 6px;
            background-color: #ffffff;
            font-size: 13px;
            color: #495057;
        }
        
        QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {
            border: 1px solid #3498db;
        }
        
        QLabel {
            color: #2c3e50;
            font-weight: 600;
            font-size: 13px;
        }
        
        QDialog {
            background-color: #ffffff;
        }
        
        QMessageBox {
            background-color: #ffffff;
        }
        """
        self.setStyleSheet(stylesheet)
