# tools/syslog_viewer_tool.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFrame, QLabel, QTextEdit, QHBoxLayout
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import socket

class SyslogViewerTool(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.syslog_thread = None
        self.is_listening = False

    def init_ui(self):
        layout = QVBoxLayout()

        # Button layout
        button_layout = QHBoxLayout()
        self.btn_start_syslog = QPushButton("Start Syslog Listener")
        self.btn_start_syslog.setStyleSheet(
            "background-color: #343b47; color: #fff; padding: 15px;"
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )
        self.btn_start_syslog.clicked.connect(self.toggle_syslog_listener)
        button_layout.addWidget(self.btn_start_syslog)

        # Reset Button
        self.btn_reset = QPushButton("Reset")
        self.btn_reset.setStyleSheet(
            "background-color: #343b47; color: #fff; padding: 15px;"
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )
        self.btn_reset.clicked.connect(self.reset_syslog_viewer_tool)
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
        output_label = QLabel("Syslog Messages:")
        output_label.setStyleSheet("font-size: 12pt; color: #fff;")
        output_layout.addWidget(output_label)

        self.syslog_output = QTextEdit()
        self.syslog_output.setReadOnly(True)
        self.syslog_output.setStyleSheet(
            "background-color: #2c313c; color: #fff; padding: 10px; font-size: 12pt;"
        )
        output_layout.addWidget(self.syslog_output)

        layout.addLayout(output_layout)

        self.setLayout(layout)

    def toggle_syslog_listener(self):
        if not self.is_listening:
            self.start_syslog_listener()
        else:
            self.stop_syslog_listener()

    def start_syslog_listener(self):
        self.syslog_output.append("Starting syslog listener on UDP port 514...")
        self.is_listening = True
        self.btn_start_syslog.setText("Stop Syslog Listener")
        self.btn_start_syslog.setStyleSheet(
            "background-color: red; color: #fff; padding: 15px;"
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )
        self.syslog_thread = SyslogListenerThread()
        self.syslog_thread.message_received.connect(self.update_syslog_output)
        self.syslog_thread.start()

    def stop_syslog_listener(self):
        self.syslog_output.append("Stopping syslog listener...")
        self.is_listening = False
        self.btn_start_syslog.setText("Start Syslog Listener")
        self.btn_start_syslog.setStyleSheet(
            "background-color: #343b47; color: #fff; padding: 15px;"
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )
        if self.syslog_thread:
            self.syslog_thread.stop()
            self.syslog_thread.wait()
            self.syslog_thread = None

    def update_syslog_output(self, message):
        self.syslog_output.append(message)

    def reset_syslog_viewer_tool(self):
        self.syslog_output.clear()
        if self.is_listening:
            self.stop_syslog_listener()

class SyslogListenerThread(QThread):
    message_received = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._is_running = True

    def run(self):
        # Bind to UDP port 514 (syslog)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', 514))
        sock.settimeout(1)
        while self._is_running:
            try:
                data, addr = sock.recvfrom(1024)
                message = data.decode('utf-8').strip()
                self.message_received.emit(f"{addr[0]}: {message}")
            except socket.timeout:
                continue
            except Exception as e:
                self.message_received.emit(f"Error: {e}")
        sock.close()

    def stop(self):
        self._is_running = False
