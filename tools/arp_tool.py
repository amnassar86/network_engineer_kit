# tools/arp_tool.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QFrame, QLabel, QTextEdit
from PyQt6.QtCore import Qt
from threads.arp_thread import ARPThread
from utils import show_error_message

class ARPTool(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Input section
        input_layout = QVBoxLayout()
        self.input_arp_ip = QLineEdit()
        self.input_arp_ip.setPlaceholderText("Enter IP for ARP")
        self.input_arp_ip.setStyleSheet(
            "padding: 10px; font-size: 12pt; color: #fff; background-color: #2c313c; border: none;")
        input_layout.addWidget(self.input_arp_ip)

        self.btn_execute_arp = QPushButton("Get ARP Entry")  # Changed to instance variable
        self.btn_execute_arp.setStyleSheet(
            "background-color: #343b47; color: #fff; padding: 15px; "
            "font-size: 12pt; border-radius: 8px; margin: 5px;")
        self.btn_execute_arp.clicked.connect(self.execute_arp_table)
        input_layout.addWidget(self.btn_execute_arp)

        # Reset Button
        btn_reset_arp = QPushButton("Reset")
        btn_reset_arp.setStyleSheet(
            "background-color: #343b47; color: #fff; padding: 15px; "
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )
        btn_reset_arp.clicked.connect(self.reset_arp_tool)
        input_layout.addWidget(btn_reset_arp)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setFrameShadow(QFrame.Shadow.Sunken)
        divider.setStyleSheet("color: #343b47;")
        input_layout.addWidget(divider)

        # Output section
        output_layout = QVBoxLayout()
        output_label = QLabel("ARP Table Results:")
        output_label.setStyleSheet("font-size: 12pt; color: #fff;")
        output_layout.addWidget(output_label)

        self.arp_output = QTextEdit()
        self.arp_output.setReadOnly(True)
        self.arp_output.setStyleSheet(
            "background-color: #2c313c; color: #fff; padding: 10px; font-size: 12pt;")
        output_layout.addWidget(self.arp_output)

        layout.addLayout(input_layout)
        layout.addLayout(output_layout)

        self.setLayout(layout)

    def reset_arp_tool(self):
        self.input_arp_ip.clear()
        self.arp_output.clear()

    def execute_arp_table(self):
        target_ip = self.input_arp_ip.text()
        if not target_ip:
            show_error_message(self, "Please enter a valid IP.")
            return

        self.arp_output.clear()
        # Disable the execute button to prevent multiple clicks
        self.btn_execute_arp.setEnabled(False)  # Access the button directly

        self.arp_thread = ARPThread(target_ip)
        self.arp_thread.output.connect(self.update_arp_output)
        self.arp_thread.finished.connect(self.arp_finished)
        self.arp_thread.start()

    def update_arp_output(self, text):
        self.arp_output.append(text)

    def arp_finished(self):
        # Re-enable the execute button
        self.btn_execute_arp.setEnabled(True)  # Access the button directly
