# tools/ping_tool.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QFrame, QLabel, QTextEdit
from PyQt6.QtCore import Qt
from threads.ping_thread import PingThread
from utils import show_error_message

class PingTool(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Input section
        input_layout = QVBoxLayout()
        self.input_ping_ip = QLineEdit()
        self.input_ping_ip.setPlaceholderText("Enter IP or Domain to Ping")
        self.input_ping_ip.setStyleSheet(
            "padding: 10px; font-size: 12pt; color: #fff; background-color: #2c313c; border: none;")
        input_layout.addWidget(self.input_ping_ip)

        self.btn_execute_ping = QPushButton("Execute Ping")  # Changed to instance variable
        self.btn_execute_ping.setStyleSheet(
            "background-color: #343b47; color: #fff; padding: 15px; "
            "font-size: 12pt; border-radius: 8px; margin: 5px;")
        self.btn_execute_ping.clicked.connect(self.execute_ping)
        input_layout.addWidget(self.btn_execute_ping)

        # Reset Button
        btn_reset_ping = QPushButton("Reset")
        btn_reset_ping.setStyleSheet(
            "background-color: #343b47; color: #fff; padding: 15px; "
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )
        btn_reset_ping.clicked.connect(self.reset_ping_tool)
        input_layout.addWidget(btn_reset_ping)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setFrameShadow(QFrame.Shadow.Sunken)
        divider.setStyleSheet("color: #343b47;")
        input_layout.addWidget(divider)

        # Output section
        output_layout = QVBoxLayout()
        output_label = QLabel("Ping Results:")
        output_label.setStyleSheet("font-size: 12pt; color: #fff;")
        output_layout.addWidget(output_label)

        self.ping_output = QTextEdit()
        self.ping_output.setReadOnly(True)
        self.ping_output.setStyleSheet(
            "background-color: #2c313c; color: #fff; padding: 10px; font-size: 12pt;")
        output_layout.addWidget(self.ping_output)

        layout.addLayout(input_layout)
        layout.addLayout(output_layout)

        self.setLayout(layout)

    def reset_ping_tool(self):
        self.input_ping_ip.clear()
        self.ping_output.clear()

    def execute_ping(self):
        target = self.input_ping_ip.text()
        if not target:
            show_error_message(self, "Please enter a valid IP or domain.")
            return

        self.ping_output.clear()
        # Disable the execute button to prevent multiple clicks
        self.btn_execute_ping.setEnabled(False)

        self.ping_thread = PingThread(target)
        self.ping_thread.output.connect(self.update_ping_output)
        self.ping_thread.finished.connect(self.ping_finished)
        self.ping_thread.start()

    def update_ping_output(self, text):
        self.ping_output.append(text)

    def ping_finished(self):
        # Re-enable the execute button
        self.btn_execute_ping.setEnabled(True)
