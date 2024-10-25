# utils.py
from PyQt6.QtWidgets import QMessageBox
import ipaddress

def show_error_message(parent, message):
    msg = QMessageBox(parent)
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setText(message)
    msg.setWindowTitle("Input Error")
    msg.setStyleSheet("""
        QMessageBox {
            background-color: #2c313c;
            color: #fff;
        }
        QPushButton {
            background-color: #343b47;
            color: #fff;
        }
    """)
    msg.exec()

def validate_ip_range(ip_range):
    try:
        start_ip, end_ip = ip_range.split('-')
        start = ipaddress.IPv4Address(start_ip.strip())
        end = ipaddress.IPv4Address(end_ip.strip())
        return start <= end
    except ValueError:
        return False
