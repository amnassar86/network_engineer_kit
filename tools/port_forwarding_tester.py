# tools/port_forwarding_tester.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QFrame, QLabel, QTextEdit, QHBoxLayout, QSpinBox
)
from PyQt6.QtCore import Qt
from threads.port_check_thread import PortCheckThread
from utils import show_error_message

class PortForwardingTester(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.is_testing = False

    def init_ui(self):
        layout = QVBoxLayout()

        # Input section
        input_layout = QVBoxLayout()

        self.input_target_ip = QLineEdit()
        self.input_target_ip.setPlaceholderText("Enter Target IP or Domain")
        self.input_target_ip.setStyleSheet(
            "padding: 10px; font-size: 12pt; color: #fff; background-color: #2c313c; border: none;"
        )
        input_layout.addWidget(self.input_target_ip)

        # Port input
        port_layout = QHBoxLayout()
        port_label = QLabel("Port:")
        port_label.setStyleSheet("font-size: 12pt; color: #fff;")
        self.port_input = QSpinBox()
        self.port_input.setRange(1, 65535)
        self.port_input.setValue(80)
        self.port_input.setStyleSheet(
            "padding: 5px; font-size: 12pt; color: #fff; background-color: #2c313c;"
        )
        port_layout.addWidget(port_label)
        port_layout.addWidget(self.port_input)
        input_layout.addLayout(port_layout)

        # Button layout
        button_layout = QHBoxLayout()
        self.btn_start_test = QPushButton("Start Test")
        self.btn_start_test.setStyleSheet(
            "background-color: #343b47; color: #fff; padding: 15px;"
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )
        self.btn_start_test.clicked.connect(self.toggle_test)
        button_layout.addWidget(self.btn_start_test)

        # Reset Button
        self.btn_reset = QPushButton("Reset")
        self.btn_reset.setStyleSheet(
            "background-color: #343b47; color: #fff; padding: 15px;"
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )
        self.btn_reset.clicked.connect(self.reset_port_forwarding_tester)
        button_layout.addWidget(self.btn_reset)

        input_layout.addLayout(button_layout)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setFrameShadow(QFrame.Shadow.Sunken)
        divider.setStyleSheet("color: #343b47;")
        input_layout.addWidget(divider)

        # Output section
        output_layout = QVBoxLayout()
        output_label = QLabel("Port Forwarding Test Results:")
        output_label.setStyleSheet("font-size: 12pt; color: #fff;")
        output_layout.addWidget(output_label)

        self.test_output = QTextEdit()
        self.test_output.setReadOnly(True)
        self.test_output.setStyleSheet(
            "background-color: #2c313c; color: #fff; padding: 10px; font-size: 12pt;"
        )
        output_layout.addWidget(self.test_output)

        layout.addLayout(input_layout)
        layout.addLayout(output_layout)

        self.setLayout(layout)

    def toggle_test(self):
        if not self.is_testing:
            self.execute_port_test()
        else:
            self.stop_port_test()

    def execute_port_test(self):
        target = self.input_target_ip.text()
        port = self.port_input.value()
        if not target:
            show_error_message(self, "Please enter a valid IP or domain.")
            return

        self.test_output.clear()
        self.is_testing = True
        self.btn_start_test.setText("Stop Test")
        self.btn_start_test.setStyleSheet(
            "background-color: red; color: #fff; padding: 15px;"
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )

        # Start the port check thread
        self.port_thread = PortCheckThread(target, port)
        self.port_thread.output.connect(self.update_test_output)
        self.port_thread.finished.connect(self.port_test_finished)
        self.port_thread.start()

    def stop_port_test(self):
        if self.port_thread and self.port_thread.isRunning():
            self.port_thread.stop()
            self.port_thread.wait()
        self.port_test_finished()

    def update_test_output(self, text):
        self.test_output.append(text)

    def port_test_finished(self):
        self.is_testing = False
        self.btn_start_test.setText("Start Test")
        self.btn_start_test.setStyleSheet(
            "background-color: #343b47; color: #fff; padding: 15px;"
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )

    def reset_port_forwarding_tester(self):
        self.input_target_ip.clear()
        self.port_input.setValue(80)
        self.test_output.clear()
        if self.is_testing:
            self.stop_port_test()
