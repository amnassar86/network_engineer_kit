# tools/packet_sniffer_tool.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QFrame, QLabel, QTextEdit, QComboBox, QCheckBox
)
from PyQt6.QtCore import Qt
from threads.packet_sniffer_thread import PacketSnifferThread
from utils import show_error_message
import scapy.all as scapy

class PacketSnifferTool(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.is_sniffing = False

    def init_ui(self):
        layout = QVBoxLayout()

        # Input section
        input_layout = QVBoxLayout()

        # Interface selection
        iface_layout = QHBoxLayout()
        iface_label = QLabel("Select Interface:")
        iface_label.setStyleSheet("font-size: 12pt; color: #fff;")
        self.iface_combo = QComboBox()
        self.iface_combo.setStyleSheet(
            "padding: 5px; font-size: 12pt; color: #fff; background-color: #2c313c;"
        )
        self.populate_interfaces()
        iface_layout.addWidget(iface_label)
        iface_layout.addWidget(self.iface_combo)
        input_layout.addLayout(iface_layout)

        # Filter input
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Enter BPF Filter (e.g., tcp port 80)")
        self.filter_input.setStyleSheet(
            "padding: 10px; font-size: 12pt; color: #fff; background-color: #2c313c; border: none;"
        )
        input_layout.addWidget(self.filter_input)

        # Promiscuous mode checkbox
        self.promiscuous_checkbox = QCheckBox("Enable Promiscuous Mode")
        self.promiscuous_checkbox.setChecked(True)
        self.promiscuous_checkbox.setStyleSheet("font-size: 12pt; color: #fff;")
        input_layout.addWidget(self.promiscuous_checkbox)

        # Button layout
        button_layout = QHBoxLayout()
        self.btn_start_sniffing = QPushButton("Start Sniffing")
        self.btn_start_sniffing.setStyleSheet(
            "background-color: #343b47; color: #fff; padding: 15px;"
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )
        self.btn_start_sniffing.clicked.connect(self.toggle_sniffing)
        button_layout.addWidget(self.btn_start_sniffing)

        # Reset Button
        self.btn_reset = QPushButton("Reset")
        self.btn_reset.setStyleSheet(
            "background-color: #343b47; color: #fff; padding: 15px;"
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )
        self.btn_reset.clicked.connect(self.reset_packet_sniffer)
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
        output_label = QLabel("Captured Packets:")
        output_label.setStyleSheet("font-size: 12pt; color: #fff;")
        output_layout.addWidget(output_label)

        self.sniff_output = QTextEdit()
        self.sniff_output.setReadOnly(True)
        self.sniff_output.setStyleSheet(
            "background-color: #2c313c; color: #fff; padding: 10px; font-size: 12pt;"
        )
        output_layout.addWidget(self.sniff_output)

        layout.addLayout(input_layout)
        layout.addLayout(output_layout)

        self.setLayout(layout)

    def populate_interfaces(self):
        interfaces = scapy.get_if_list()
        self.iface_combo.addItems(interfaces)

    def toggle_sniffing(self):
        if not self.is_sniffing:
            self.start_sniffing()
        else:
            self.stop_sniffing()

    def start_sniffing(self):
        iface = self.iface_combo.currentText()
        bpf_filter = self.filter_input.text()
        promiscuous = self.promiscuous_checkbox.isChecked()

        self.sniff_output.clear()
        self.is_sniffing = True
        self.btn_start_sniffing.setText("Stop Sniffing")
        self.btn_start_sniffing.setStyleSheet(
            "background-color: red; color: #fff; padding: 15px;"
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )

        # Start the packet sniffer thread
        self.sniffer_thread = PacketSnifferThread(iface, bpf_filter, promiscuous)
        self.sniffer_thread.output.connect(self.update_sniff_output)
        self.sniffer_thread.finished.connect(self.sniffing_finished)
        self.sniffer_thread.start()

    def stop_sniffing(self):
        if self.sniffer_thread and self.sniffer_thread.isRunning():
            self.sniffer_thread.stop()
            self.sniffer_thread.wait()
        self.sniffing_finished()

    def update_sniff_output(self, text):
        self.sniff_output.append(text)

    def sniffing_finished(self):
        self.is_sniffing = False
        self.btn_start_sniffing.setText("Start Sniffing")
        self.btn_start_sniffing.setStyleSheet(
            "background-color: #343b47; color: #fff; padding: 15px;"
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )

    def reset_packet_sniffer(self):
        self.filter_input.clear()
        self.sniff_output.clear()
        if self.is_sniffing:
            self.stop_sniffing()
