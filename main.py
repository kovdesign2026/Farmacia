import sys
from PyQt5.QtWidgets import QApplication
from DependencyContainer import DependencyContainer
from ui.MainWindow import MainWindow


def main():
    app = QApplication(sys.argv)
    container = DependencyContainer()
    window = MainWindow(container.controllers)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
