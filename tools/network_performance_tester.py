# tools/network_performance_tester.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QFrame, QLabel, QTextEdit, QHBoxLayout
)
from PyQt6.QtCore import Qt
from threads.network_performance_thread import NetworkPerformanceThread
from utils import show_error_message

class NetworkPerformanceTester(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.is_testing = False

    def init_ui(self):
        layout = QVBoxLayout()

        # Instructions
        instructions = QLabel("Ensure iperf3 is installed on both client and server. Start the server with 'iperf3 -s'.")
        instructions.setStyleSheet("font-size: 10pt; color: #fff;")
        layout.addWidget(instructions)

        # Input section
        input_layout = QVBoxLayout()

        self.input_server_ip = QLineEdit()
        self.input_server_ip.setPlaceholderText("Enter Server IP Address")
        self.input_server_ip.setStyleSheet(
            "padding: 10px; font-size: 12pt; color: #fff; background-color: #2c313c; border: none;"
        )
        input_layout.addWidget(self.input_server_ip)

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
        self.btn_reset.clicked.connect(self.reset_network_performance_tester)
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
        output_label = QLabel("Network Performance Test Results:")
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
            self.execute_performance_test()
        else:
            self.stop_performance_test()

    def execute_performance_test(self):
        server_ip = self.input_server_ip.text()
        if not server_ip:
            show_error_message(self, "Please enter a valid server IP address.")
            return

        self.test_output.clear()
        self.is_testing = True
        self.btn_start_test.setText("Stop Test")
        self.btn_start_test.setStyleSheet(
            "background-color: red; color: #fff; padding: 15px;"
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )

        # Start the performance test thread
        self.performance_thread = NetworkPerformanceThread(server_ip)
        self.performance_thread.output.connect(self.update_test_output)
        self.performance_thread.finished.connect(self.performance_test_finished)
        self.performance_thread.start()

    def stop_performance_test(self):
        if self.performance_thread and self.performance_thread.isRunning():
            self.performance_thread.stop()
            self.performance_thread.wait()
        self.performance_test_finished()

    def update_test_output(self, text):
        self.test_output.append(text)

    def performance_test_finished(self):
        self.is_testing = False
        self.btn_start_test.setText("Start Test")
        self.btn_start_test.setStyleSheet(
            "background-color: #343b47; color: #fff; padding: 15px;"
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )

    def reset_network_performance_tester(self):
        self.input_server_ip.clear()
        self.test_output.clear()
        if self.is_testing:
            self.stop_performance_test()
