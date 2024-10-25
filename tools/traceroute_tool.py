# tools/traceroute_tool.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QFrame, QLabel, QTextEdit
from PyQt6.QtCore import Qt
from threads.traceroute_thread import TracerouteThread
from utils import show_error_message

class TracerouteTool(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Input section
        input_layout = QVBoxLayout()
        self.input_traceroute_ip = QLineEdit()
        self.input_traceroute_ip.setPlaceholderText("Enter IP or Domain to Traceroute")
        self.input_traceroute_ip.setStyleSheet(
            "padding: 10px; font-size: 12pt; color: #fff; background-color: #2c313c; border: none;")
        input_layout.addWidget(self.input_traceroute_ip)

        self.btn_execute_traceroute = QPushButton("Execute Traceroute")  # Changed to instance variable
        self.btn_execute_traceroute.setStyleSheet(
            "background-color: #343b47; color: #fff; padding: 15px; "
            "font-size: 12pt; border-radius: 8px; margin: 5px;")
        self.btn_execute_traceroute.clicked.connect(self.execute_traceroute)
        input_layout.addWidget(self.btn_execute_traceroute)

        # Reset Button
        btn_reset_traceroute = QPushButton("Reset")
        btn_reset_traceroute.setStyleSheet(
            "background-color: #343b47; color: #fff; padding: 15px; "
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )
        btn_reset_traceroute.clicked.connect(self.reset_traceroute_tool)
        input_layout.addWidget(btn_reset_traceroute)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setFrameShadow(QFrame.Shadow.Sunken)
        divider.setStyleSheet("color: #343b47;")
        input_layout.addWidget(divider)

        # Output section
        output_layout = QVBoxLayout()
        output_label = QLabel("Traceroute Results:")
        output_label.setStyleSheet("font-size: 12pt; color: #fff;")
        output_layout.addWidget(output_label)

        self.traceroute_output = QTextEdit()
        self.traceroute_output.setReadOnly(True)
        self.traceroute_output.setStyleSheet(
            "background-color: #2c313c; color: #fff; padding: 10px; font-size: 12pt;")
        output_layout.addWidget(self.traceroute_output)

        layout.addLayout(input_layout)
        layout.addLayout(output_layout)

        self.setLayout(layout)

    def reset_traceroute_tool(self):
        self.input_traceroute_ip.clear()
        self.traceroute_output.clear()

    def execute_traceroute(self):
        target = self.input_traceroute_ip.text()
        if not target:
            show_error_message(self, "Please enter a valid IP or domain.")
            return

        self.traceroute_output.clear()
        # Disable the execute button to prevent multiple clicks
        self.btn_execute_traceroute.setEnabled(False)

        self.traceroute_thread = TracerouteThread(target)
        self.traceroute_thread.output.connect(self.update_traceroute_output)
        self.traceroute_thread.finished.connect(self.traceroute_finished)
        self.traceroute_thread.start()

    def update_traceroute_output(self, text):
        self.traceroute_output.append(text)

    def traceroute_finished(self):
        # Re-enable the execute button
        self.btn_execute_traceroute.setEnabled(True)
