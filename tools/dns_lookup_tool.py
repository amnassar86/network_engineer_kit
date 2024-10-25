# tools/dns_lookup_tool.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QFrame, QLabel, QTextEdit, QComboBox
)
from PyQt6.QtCore import Qt
from threads.dns_lookup_thread import DNSLookupThread
from utils import show_error_message

class DNSLookupTool(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.is_querying = False

    def init_ui(self):
        layout = QVBoxLayout()

        # Input section
        input_layout = QVBoxLayout()

        self.input_domain = QLineEdit()
        self.input_domain.setPlaceholderText("Enter Domain Name (e.g., example.com)")
        self.input_domain.setStyleSheet(
            "padding: 10px; font-size: 12pt; color: #fff; background-color: #2c313c; border: none;"
        )
        input_layout.addWidget(self.input_domain)

        self.record_type_combo = QComboBox()
        self.record_type_combo.addItems(["A", "AAAA", "CNAME", "MX", "NS", "TXT", "PTR", "SOA"])
        self.record_type_combo.setStyleSheet(
            "padding: 10px; font-size: 12pt; color: #fff; background-color: #2c313c;"
        )
        input_layout.addWidget(self.record_type_combo)

        self.btn_execute_dns_lookup = QPushButton("Execute DNS Lookup")
        self.btn_execute_dns_lookup.setStyleSheet(
            "background-color: #343b47; color: #fff; padding: 15px;"
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )
        self.btn_execute_dns_lookup.clicked.connect(self.execute_dns_lookup)
        input_layout.addWidget(self.btn_execute_dns_lookup)

        # Reset Button
        btn_reset_dns_lookup = QPushButton("Reset")
        btn_reset_dns_lookup.setStyleSheet(
            "background-color: #343b47; color: #fff; padding: 15px;"
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )
        btn_reset_dns_lookup.clicked.connect(self.reset_dns_lookup_tool)
        input_layout.addWidget(btn_reset_dns_lookup)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setFrameShadow(QFrame.Shadow.Sunken)
        divider.setStyleSheet("color: #343b47;")
        input_layout.addWidget(divider)

        # Output section
        output_layout = QVBoxLayout()
        output_label = QLabel("DNS Lookup Results:")
        output_label.setStyleSheet("font-size: 12pt; color: #fff;")
        output_layout.addWidget(output_label)

        self.dns_output = QTextEdit()
        self.dns_output.setReadOnly(True)
        self.dns_output.setStyleSheet(
            "background-color: #2c313c; color: #fff; padding: 10px; font-size: 12pt;"
        )
        output_layout.addWidget(self.dns_output)

        layout.addLayout(input_layout)
        layout.addLayout(output_layout)

        self.setLayout(layout)

    def reset_dns_lookup_tool(self):
        self.input_domain.clear()
        self.dns_output.clear()
        self.is_querying = False
        self.btn_execute_dns_lookup.setEnabled(True)

    def execute_dns_lookup(self):
        if self.is_querying:
            return  # Prevent multiple clicks

        domain = self.input_domain.text()
        record_type = self.record_type_combo.currentText()

        if not domain:
            show_error_message(self, "Please enter a valid domain name.")
            return

        self.dns_output.clear()
        self.btn_execute_dns_lookup.setEnabled(False)
        self.is_querying = True

        # Start the DNS lookup thread
        self.dns_thread = DNSLookupThread(domain, record_type)
        self.dns_thread.output.connect(self.update_dns_output)
        self.dns_thread.finished.connect(self.dns_lookup_finished)
        self.dns_thread.start()

    def update_dns_output(self, text):
        self.dns_output.append(text)

    def dns_lookup_finished(self):
        self.is_querying = False
        self.btn_execute_dns_lookup.setEnabled(True)
