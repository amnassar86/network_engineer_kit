# tools/netstat_viewer_tool.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFrame, QLabel, QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt
import psutil
import socket  # Import the socket module

class NetstatViewerTool(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Refresh Button
        btn_refresh = QPushButton("Refresh Connections")
        btn_refresh.setStyleSheet(
            "background-color: #343b47; color: #fff; padding: 15px;"
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )
        btn_refresh.clicked.connect(self.display_connections)
        layout.addWidget(btn_refresh)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setFrameShadow(QFrame.Shadow.Sunken)
        divider.setStyleSheet("color: #343b47;")
        layout.addWidget(divider)

        # Output section
        output_layout = QVBoxLayout()
        output_label = QLabel("Active Connections:")
        output_label.setStyleSheet("font-size: 12pt; color: #fff;")
        output_layout.addWidget(output_label)

        self.connection_table = QTableWidget()
        self.connection_table.setColumnCount(5)
        self.connection_table.setHorizontalHeaderLabels(["Protocol", "Local Address", "Remote Address", "Status", "PID"])
        self.connection_table.setStyleSheet("""
            QTableWidget {
                background-color: #2c313c;
                color: #fff;
                gridline-color: #343b47;
            }
            QHeaderView::section {
                background-color: #343b47;
                color: #fff;
                padding: 4px;
                font-size: 10pt;
            }
        """)
        self.connection_table.horizontalHeader().setStretchLastSection(True)
        self.connection_table.verticalHeader().setVisible(False)
        output_layout.addWidget(self.connection_table)

        layout.addLayout(output_layout)

        self.setLayout(layout)

        # Display connections on initialization
        self.display_connections()

    def display_connections(self):
        self.connection_table.setRowCount(0)
        connections = psutil.net_connections()
        for conn in connections:
            # Use socket constants instead of psutil constants
            if conn.type == socket.SOCK_STREAM:
                protocol = "TCP"
            elif conn.type == socket.SOCK_DGRAM:
                protocol = "UDP"
            else:
                protocol = "Other"

            laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else ""
            raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else ""
            status = conn.status
            pid = str(conn.pid) if conn.pid else ""

            row_position = self.connection_table.rowCount()
            self.connection_table.insertRow(row_position)
            self.connection_table.setItem(row_position, 0, QTableWidgetItem(protocol))
            self.connection_table.setItem(row_position, 1, QTableWidgetItem(laddr))
            self.connection_table.setItem(row_position, 2, QTableWidgetItem(raddr))
            self.connection_table.setItem(row_position, 3, QTableWidgetItem(status))
            self.connection_table.setItem(row_position, 4, QTableWidgetItem(pid))
