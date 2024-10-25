# main.py

from PyQt6.QtWidgets import QApplication
from network_toolkit_app import NetworkToolkitApp
import sys
from database import initialize_database

if __name__ == "__main__":
    initialize_database()
    app = QApplication(sys.argv)
    window = NetworkToolkitApp()
    window.show()
    sys.exit(app.exec())