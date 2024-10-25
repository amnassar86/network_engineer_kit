# tools/snmp_manager_tool.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QFrame, QLabel, QTextEdit
)
from PyQt6.QtCore import Qt
from threads.snmp_thread import SNMPThread
from utils import show_error_message

class SNMPManagerTool(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.is_querying = False

    def init_ui(self):
        layout = QVBoxLayout()

        # Input section
        input_layout = QVBoxLayout()

        self.input_ip = QLineEdit()
        self.input_ip.setPlaceholderText("Enter Device IP Address")
        self.input_ip.setStyleSheet(
            "padding: 10px; font-size: 12pt; color: #fff; background-color: #2c313c; border: none;"
        )
        input_layout.addWidget(self.input_ip)

        self.input_community = QLineEdit()
        self.input_community.setPlaceholderText("Enter SNMP Community String (default: public)")
        self.input_community.setStyleSheet(
            "padding: 10px; font-size: 12pt; color: #fff; background-color: #2c313c; border: none;"
        )
        input_layout.addWidget(self.input_community)

        self.input_oid = QLineEdit()
        self.input_oid.setPlaceholderText("Enter OID (e.g., 1.3.6.1.2.1.1.1.0 for sysDescr)")
        self.input_oid.setStyleSheet(
            "padding: 10px; font-size: 12pt; color: #fff; background-color: #2c313c; border: none;"
        )
        input_layout.addWidget(self.input_oid)

        self.btn_execute_snmp = QPushButton("Execute SNMP Query")
        self.btn_execute_snmp.setStyleSheet(
            "background-color: #343b47; color: #fff; padding: 15px;"
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )
        self.btn_execute_snmp.clicked.connect(self.execute_snmp_query)
        input_layout.addWidget(self.btn_execute_snmp)

        # Reset Button
        btn_reset_snmp = QPushButton("Reset")
        btn_reset_snmp.setStyleSheet(
            "background-color: #343b47; color: #fff; padding: 15px;"
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )
        btn_reset_snmp.clicked.connect(self.reset_snmp_tool)
        input_layout.addWidget(btn_reset_snmp)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setFrameShadow(QFrame.Shadow.Sunken)
        divider.setStyleSheet("color: #343b47;")
        input_layout.addWidget(divider)

        # Output section
        output_layout = QVBoxLayout()
        output_label = QLabel("SNMP Query Results:")
        output_label.setStyleSheet("font-size: 12pt; color: #fff;")
        output_layout.addWidget(output_label)

        self.snmp_output = QTextEdit()
        self.snmp_output.setReadOnly(True)
        self.snmp_output.setStyleSheet(
            "background-color: #2c313c; color: #fff; padding: 10px; font-size: 12pt;"
        )
        output_layout.addWidget(self.snmp_output)

        layout.addLayout(input_layout)
        layout.addLayout(output_layout)

        self.setLayout(layout)

    def reset_snmp_tool(self):
        self.input_ip.clear()
        self.input_community.clear()
        self.input_oid.clear()
        self.snmp_output.clear()
        self.is_querying = False
        self.btn_execute_snmp.setEnabled(True)

    def execute_snmp_query(self):
        if self.is_querying:
            return  # Prevent multiple clicks

        ip_address = self.input_ip.text()
        community = self.input_community.text() or "public"
        oid = self.input_oid.text()

        if not ip_address or not oid:
            show_error_message(self, "Please enter a valid IP address and OID.")
            return

        self.snmp_output.clear()
        self.btn_execute_snmp.setEnabled(False)
        self.is_querying = True

        # Start the SNMP query thread
        self.snmp_thread = SNMPThread(ip_address, community, oid)
        self.snmp_thread.output.connect(self.update_snmp_output)
        self.snmp_thread.finished.connect(self.snmp_query_finished)
        self.snmp_thread.start()

    def update_snmp_output(self, text):
        self.snmp_output.append(text)

    def snmp_query_finished(self):
        self.is_querying = False
        self.btn_execute_snmp.setEnabled(True)
