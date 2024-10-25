# tools/latency_jitter_tool.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QFrame, QLabel, QTextEdit, QHBoxLayout
)
from PyQt6.QtCore import Qt
from threads.latency_jitter_thread import LatencyJitterThread
from utils import show_error_message

class LatencyJitterTool(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.is_monitoring = False

    def init_ui(self):
        layout = QVBoxLayout()

        # Input section
        input_layout = QVBoxLayout()
        self.input_target_ip = QLineEdit()
        self.input_target_ip.setPlaceholderText("Enter IP or Domain to Monitor")
        self.input_target_ip.setStyleSheet(
            "padding: 10px; font-size: 12pt; color: #fff; background-color: #2c313c; border: none;"
        )
        input_layout.addWidget(self.input_target_ip)

        # Button layout
        button_layout = QHBoxLayout()
        self.btn_start_monitoring = QPushButton("Start Monitoring")
        self.btn_start_monitoring.setStyleSheet(
            "background-color: #343b47; color: #fff; padding: 15px;"
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )
        self.btn_start_monitoring.clicked.connect(self.toggle_monitoring)
        button_layout.addWidget(self.btn_start_monitoring)

        # Reset Button
        self.btn_reset = QPushButton("Reset")
        self.btn_reset.setStyleSheet(
            "background-color: #343b47; color: #fff; padding: 15px;"
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )
        self.btn_reset.clicked.connect(self.reset_latency_jitter_tool)
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
        output_label = QLabel("Latency and Jitter Results:")
        output_label.setStyleSheet("font-size: 12pt; color: #fff;")
        output_layout.addWidget(output_label)

        self.latency_output = QTextEdit()
        self.latency_output.setReadOnly(True)
        self.latency_output.setStyleSheet(
            "background-color: #2c313c; color: #fff; padding: 10px; font-size: 12pt;"
        )
        output_layout.addWidget(self.latency_output)

        layout.addLayout(input_layout)
        layout.addLayout(output_layout)

        self.setLayout(layout)

    def toggle_monitoring(self):
        if not self.is_monitoring:
            self.execute_latency_jitter_monitor()
        else:
            self.stop_latency_jitter_monitor()

    def execute_latency_jitter_monitor(self):
        target = self.input_target_ip.text()
        if not target:
            show_error_message(self, "Please enter a valid IP or domain.")
            return

        self.latency_output.clear()
        self.is_monitoring = True
        self.btn_start_monitoring.setText("Stop Monitoring")
        self.btn_start_monitoring.setStyleSheet(
            "background-color: red; color: #fff; padding: 15px;"
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )

        # Start the latency and jitter monitoring thread
        self.latency_thread = LatencyJitterThread(target)
        self.latency_thread.output.connect(self.update_latency_output)
        self.latency_thread.finished.connect(self.latency_jitter_finished)
        self.latency_thread.start()

    def stop_latency_jitter_monitor(self):
        if self.latency_thread and self.latency_thread.isRunning():
            self.latency_thread.stop()
            self.latency_thread.wait()
        self.latency_jitter_finished()

    def update_latency_output(self, text):
        self.latency_output.append(text)

    def latency_jitter_finished(self):
        self.is_monitoring = False
        self.btn_start_monitoring.setText("Start Monitoring")
        self.btn_start_monitoring.setStyleSheet(
            "background-color: #343b47; color: #fff; padding: 15px;"
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )

    def reset_latency_jitter_tool(self):
        self.input_target_ip.clear()
        self.latency_output.clear()
        if self.is_monitoring:
            self.stop_latency_jitter_monitor()
