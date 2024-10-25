# tools/network_interface_tool.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFrame, QLabel, QTextEdit
)
from PyQt6.QtCore import Qt
import psutil
import socket

class NetworkInterfaceTool(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Refresh Button
        btn_refresh = QPushButton("Refresh Interfaces")
        btn_refresh.setStyleSheet(
            "background-color: #343b47; color: #fff; padding: 15px;"
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )
        btn_refresh.clicked.connect(self.display_interfaces)
        layout.addWidget(btn_refresh)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setFrameShadow(QFrame.Shadow.Sunken)
        divider.setStyleSheet("color: #343b47;")
        layout.addWidget(divider)

        # Output section
        output_layout = QVBoxLayout()
        output_label = QLabel("Network Interfaces:")
        output_label.setStyleSheet("font-size: 12pt; color: #fff;")
        output_layout.addWidget(output_label)

        self.interface_output = QTextEdit()
        self.interface_output.setReadOnly(True)
        self.interface_output.setStyleSheet(
            "background-color: #2c313c; color: #fff; padding: 10px; font-size: 12pt;"
        )
        output_layout.addWidget(self.interface_output)

        layout.addLayout(output_layout)

        self.setLayout(layout)

        # Display interfaces on initialization
        self.display_interfaces()

    def display_interfaces(self):
        self.interface_output.clear()
        addrs = psutil.net_if_addrs()
        stats = psutil.net_if_stats()

        # Try to define AF_LINK or AF_PACKET for MAC addresses
        try:
            AF_LINK = socket.AF_LINK
        except AttributeError:
            try:
                AF_LINK = socket.AF_PACKET
            except AttributeError:
                AF_LINK = None

        for iface_name, iface_addrs in addrs.items():
            self.interface_output.append(f"Interface: {iface_name}")
            is_up = stats[iface_name].isup if iface_name in stats else False
            self.interface_output.append(f"Status: {'Up' if is_up else 'Down'}")
            for addr in iface_addrs:
                if addr.family == socket.AF_INET:
                    self.interface_output.append(f"  IP Address: {addr.address}")
                    self.interface_output.append(f"  Netmask: {addr.netmask}")
                    if addr.broadcast:
                        self.interface_output.append(f"  Broadcast IP: {addr.broadcast}")
                elif addr.family == socket.AF_INET6:
                    self.interface_output.append(f"  IPv6 Address: {addr.address}")
                    self.interface_output.append(f"  Netmask: {addr.netmask}")
                    if addr.broadcast:
                        self.interface_output.append(f"  Broadcast IP: {addr.broadcast}")
                elif AF_LINK and addr.family == AF_LINK:
                    self.interface_output.append(f"  MAC Address: {addr.address}")
                else:
                    self.interface_output.append(f"  Other Address ({addr.family}): {addr.address}")
            self.interface_output.append("")
