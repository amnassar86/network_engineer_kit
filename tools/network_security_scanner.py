# tools/network_security_scanner.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QFrame, QLabel, QTextEdit, QHBoxLayout
)
from PyQt6.QtCore import Qt
from threads.security_scan_thread import SecurityScanThread
from utils import show_error_message

class NetworkSecurityScanner(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.is_scanning = False

    def init_ui(self):
        layout = QVBoxLayout()

        # Input section
        input_layout = QVBoxLayout()

        self.input_target = QLineEdit()
        self.input_target.setPlaceholderText("Enter Target IP or Domain")
        self.input_target.setStyleSheet(
            "padding: 10px; font-size: 12pt; color: #fff; background-color: #2c313c; border: none;"
        )
        input_layout.addWidget(self.input_target)

        # Button layout
        button_layout = QHBoxLayout()
        self.btn_start_scan = QPushButton("Start Security Scan")
        self.btn_start_scan.setStyleSheet(
            "background-color: #343b47; color: #fff; padding: 15px;"
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )
        self.btn_start_scan.clicked.connect(self.toggle_scanning)
        button_layout.addWidget(self.btn_start_scan)

        # Reset Button
        self.btn_reset = QPushButton("Reset")
        self.btn_reset.setStyleSheet(
            "background-color: #343b47; color: #fff; padding: 15px;"
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )
        self.btn_reset.clicked.connect(self.reset_security_scanner)
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
        output_label = QLabel("Security Scan Results:")
        output_label.setStyleSheet("font-size: 12pt; color: #fff;")
        output_layout.addWidget(output_label)

        self.scan_output = QTextEdit()
        self.scan_output.setReadOnly(True)
        self.scan_output.setStyleSheet(
            "background-color: #2c313c; color: #fff; padding: 10px; font-size: 12pt;"
        )
        output_layout.addWidget(self.scan_output)

        layout.addLayout(input_layout)
        layout.addLayout(output_layout)

        self.setLayout(layout)

    def toggle_scanning(self):
        if not self.is_scanning:
            self.start_scanning()
        else:
            self.stop_scanning()

    def start_scanning(self):
        target = self.input_target.text()
        if not target:
            show_error_message(self, "Please enter a valid target.")
            return

        self.scan_output.clear()
        self.is_scanning = True
        self.btn_start_scan.setText("Stop Security Scan")
        self.btn_start_scan.setStyleSheet(
            "background-color: red; color: #fff; padding: 15px;"
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )

        # Start the security scan thread
        self.scan_thread = SecurityScanThread(target)
        self.scan_thread.output.connect(self.update_scan_output)
        self.scan_thread.finished.connect(self.scanning_finished)
        self.scan_thread.start()

    def stop_scanning(self):
        if self.scan_thread and self.scan_thread.isRunning():
            self.scan_thread.stop()
            self.scan_thread.wait()
        self.scanning_finished()

    def update_scan_output(self, text):
        self.scan_output.append(text)

    def scanning_finished(self):
        self.is_scanning = False
        self.btn_start_scan.setText("Start Security Scan")
        self.btn_start_scan.setStyleSheet(
            "background-color: #343b47; color: #fff; padding: 15px;"
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )

    def reset_security_scanner(self):
        self.input_target.clear()
        self.scan_output.clear()
        if self.is_scanning:
            self.stop_scanning()
