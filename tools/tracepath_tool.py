# tools/tracepath_tool.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QFrame, QLabel, QTextEdit
)
from PyQt6.QtCore import Qt
from threads.tracepath_thread import TracepathThread
from utils import show_error_message
import platform

class TracepathTool(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.is_tracing = False

    def init_ui(self):
        layout = QVBoxLayout()

        # Input section
        input_layout = QVBoxLayout()
        self.input_tracepath_ip = QLineEdit()
        self.input_tracepath_ip.setPlaceholderText("Enter IP or Domain to Tracepath")
        self.input_tracepath_ip.setStyleSheet(
            "padding: 10px; font-size: 12pt; color: #fff; background-color: #2c313c; border: none;")
        input_layout.addWidget(self.input_tracepath_ip)

        self.btn_execute_tracepath = QPushButton("Execute Tracepath")
        self.btn_execute_tracepath.setStyleSheet(
            "background-color: #343b47; color: #fff; padding: 15px;"
            "font-size: 12pt; border-radius: 8px; margin: 5px;")
        self.btn_execute_tracepath.clicked.connect(self.execute_tracepath)
        input_layout.addWidget(self.btn_execute_tracepath)

        # Reset Button
        btn_reset_tracepath = QPushButton("Reset")
        btn_reset_tracepath.setStyleSheet(
            "background-color: #343b47; color: #fff; padding: 15px;"
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )
        btn_reset_tracepath.clicked.connect(self.reset_tracepath_tool)
        input_layout.addWidget(btn_reset_tracepath)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setFrameShadow(QFrame.Shadow.Sunken)
        divider.setStyleSheet("color: #343b47;")
        input_layout.addWidget(divider)

        # Output section
        output_layout = QVBoxLayout()
        output_label = QLabel("Tracepath Results:")
        output_label.setStyleSheet("font-size: 12pt; color: #fff;")
        output_layout.addWidget(output_label)

        self.tracepath_output = QTextEdit()
        self.tracepath_output.setReadOnly(True)
        self.tracepath_output.setStyleSheet(
            "background-color: #2c313c; color: #fff; padding: 10px; font-size: 12pt;")
        output_layout.addWidget(self.tracepath_output)

        layout.addLayout(input_layout)
        layout.addLayout(output_layout)

        self.setLayout(layout)

    def reset_tracepath_tool(self):
        self.input_tracepath_ip.clear()
        self.tracepath_output.clear()
        self.is_tracing = False
        self.btn_execute_tracepath.setEnabled(True)

    def execute_tracepath(self):
        if self.is_tracing:
            return  # Prevent multiple clicks

        target = self.input_tracepath_ip.text()
        if not target:
            show_error_message(self, "Please enter a valid IP or domain.")
            return

        self.tracepath_output.clear()
        self.btn_execute_tracepath.setEnabled(False)
        self.is_tracing = True

        # Start the tracepath thread
        self.tracepath_thread = TracepathThread(target)
        self.tracepath_thread.output.connect(self.update_tracepath_output)
        self.tracepath_thread.finished.connect(self.tracepath_finished)
        self.tracepath_thread.start()

    def update_tracepath_output(self, text):
        self.tracepath_output.append(text)

    def tracepath_finished(self):
        self.is_tracing = False
        self.btn_execute_tracepath.setEnabled(True)
