# tools/network_diagram_tool.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFrame, QLabel, QTextEdit, QLineEdit, QFileDialog
)
from PyQt6.QtCore import Qt
from threads.network_diagram_thread import NetworkDiagramThread
from utils import show_error_message
import os

class NetworkDiagramTool(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.is_generating = False

    def init_ui(self):
        layout = QVBoxLayout()

        # Input section
        input_layout = QVBoxLayout()
        self.input_network_range = QLineEdit()
        self.input_network_range.setPlaceholderText("Enter Network Range (e.g., 192.168.1.0/24)")
        self.input_network_range.setStyleSheet(
            "padding: 10px; font-size: 12pt; color: #fff; background-color: #2c313c; border: none;"
        )
        input_layout.addWidget(self.input_network_range)

        self.btn_generate_diagram = QPushButton("Generate Network Diagram")
        self.btn_generate_diagram.setStyleSheet(
            "background-color: #343b47; color: #fff; padding: 15px; "
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )
        self.btn_generate_diagram.clicked.connect(self.generate_network_diagram)
        input_layout.addWidget(self.btn_generate_diagram)

        # Reset Button
        btn_reset_diagram = QPushButton("Reset")
        btn_reset_diagram.setStyleSheet(
            "background-color: #343b47; color: #fff; padding: 15px; "
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )
        btn_reset_diagram.clicked.connect(self.reset_network_diagram_tool)
        input_layout.addWidget(btn_reset_diagram)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setFrameShadow(QFrame.Shadow.Sunken)
        divider.setStyleSheet("color: #343b47;")
        input_layout.addWidget(divider)

        # Output section
        output_layout = QVBoxLayout()
        output_label = QLabel("Network Diagram Generation Log:")
        output_label.setStyleSheet("font-size: 12pt; color: #fff;")
        output_layout.addWidget(output_label)

        self.diagram_output = QTextEdit()
        self.diagram_output.setReadOnly(True)
        self.diagram_output.setStyleSheet(
            "background-color: #2c313c; color: #fff; padding: 10px; font-size: 12pt;"
        )
        output_layout.addWidget(self.diagram_output)

        layout.addLayout(input_layout)
        layout.addLayout(output_layout)

        self.setLayout(layout)

    def reset_network_diagram_tool(self):
        self.input_network_range.clear()
        self.diagram_output.clear()
        self.is_generating = False
        self.btn_generate_diagram.setEnabled(True)

    def generate_network_diagram(self):
        if self.is_generating:
            return  # Prevent multiple clicks

        network_range = self.input_network_range.text()
        if not network_range:
            show_error_message(self, "Please enter a valid network range.")
            return

        self.diagram_output.clear()
        self.btn_generate_diagram.setEnabled(False)
        self.is_generating = True

        # Start the network diagram generation thread
        self.diagram_thread = NetworkDiagramThread(network_range)
        self.diagram_thread.output.connect(self.update_diagram_output)
        self.diagram_thread.finished.connect(self.diagram_generation_finished)
        self.diagram_thread.start()

    def update_diagram_output(self, text):
        self.diagram_output.append(text)

    def diagram_generation_finished(self, diagram_path):
        self.is_generating = False
        self.btn_generate_diagram.setEnabled(True)
        if diagram_path:
            self.diagram_output.append(f"\nNetwork diagram saved to: {diagram_path}")
        else:
            self.diagram_output.append("\nNetwork diagram generation failed.")
