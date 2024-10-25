# tools/wifi_analyzer_tool.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFrame, QLabel, QTableWidget, QTableWidgetItem, QHBoxLayout
)
from PyQt6.QtCore import Qt
from threads.wifi_scan_thread import WifiScanThread
from utils import show_error_message

class WifiAnalyzerTool(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.is_scanning = False

    def init_ui(self):
        layout = QVBoxLayout()

        # Button layout
        button_layout = QHBoxLayout()
        self.btn_scan_wifi = QPushButton("Scan Wi-Fi Networks")
        self.btn_scan_wifi.setStyleSheet(
            "background-color: #343b47; color: #fff; padding: 15px;"
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )
        self.btn_scan_wifi.clicked.connect(self.execute_wifi_scan)
        button_layout.addWidget(self.btn_scan_wifi)

        # Reset Button
        self.btn_reset = QPushButton("Reset")
        self.btn_reset.setStyleSheet(
            "background-color: #343b47; color: #fff; padding: 15px;"
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )
        self.btn_reset.clicked.connect(self.reset_wifi_analyzer_tool)
        button_layout.addWidget(self.btn_reset)

        layout.addLayout(button_layout)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setFrameShadow(QFrame.Shadow.Sunken)
        divider.setStyleSheet("color: #343b47;")
        layout.addWidget(divider)

        # Output section
        output_layout = QVBoxLayout()
        output_label = QLabel("Available Wi-Fi Networks:")
        output_label.setStyleSheet("font-size: 12pt; color: #fff;")
        output_layout.addWidget(output_label)

        self.wifi_table = QTableWidget()
        self.wifi_table.setColumnCount(4)
        self.wifi_table.setHorizontalHeaderLabels(["SSID", "BSSID", "Signal Strength", "Channel"])
        self.wifi_table.setStyleSheet("""
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
        self.wifi_table.horizontalHeader().setStretchLastSection(True)
        self.wifi_table.verticalHeader().setVisible(False)
        output_layout.addWidget(self.wifi_table)

        layout.addLayout(output_layout)

        self.setLayout(layout)

    def execute_wifi_scan(self):
        if self.is_scanning:
            return  # Prevent multiple clicks

        self.wifi_table.setRowCount(0)
        self.btn_scan_wifi.setEnabled(False)
        self.is_scanning = True

        # Start the Wi-Fi scan thread
        self.wifi_thread = WifiScanThread()
        self.wifi_thread.output.connect(self.update_wifi_table)
        self.wifi_thread.finished.connect(self.wifi_scan_finished)
        self.wifi_thread.start()

    def update_wifi_table(self, ssid, bssid, signal_strength, channel):
        row_position = self.wifi_table.rowCount()
        self.wifi_table.insertRow(row_position)
        self.wifi_table.setItem(row_position, 0, QTableWidgetItem(ssid))
        self.wifi_table.setItem(row_position, 1, QTableWidgetItem(bssid))
        self.wifi_table.setItem(row_position, 2, QTableWidgetItem(signal_strength))
        self.wifi_table.setItem(row_position, 3, QTableWidgetItem(channel))

    def wifi_scan_finished(self):
        self.is_scanning = False
        self.btn_scan_wifi.setEnabled(True)

    def reset_wifi_analyzer_tool(self):
        self.wifi_table.setRowCount(0)
