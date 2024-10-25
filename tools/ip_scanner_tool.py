# tools/ip_scanner_tool.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTextEdit, QLabel
)
from PyQt6.QtCore import Qt, QThreadPool, QRunnable, pyqtSlot, pyqtSignal, QObject
from utils import show_error_message
import ipaddress
from scapy.all import ARP, Ether, srp
import threading
import socket

class IPScannerTool(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.threadpool = QThreadPool()
        self.lock = threading.Lock()
        self.devices_found = []

    def init_ui(self):
        layout = QVBoxLayout()

        # Input section
        input_layout = QHBoxLayout()

        self.input_network = QLineEdit()
        self.input_network.setPlaceholderText("Enter Network (e.g., 192.168.1.0/24)")
        self.input_network.setStyleSheet(
            "padding: 10px; font-size: 12pt; color: #000; background-color: #fff; border: 1px solid #ccc;"
        )
        input_layout.addWidget(self.input_network)

        self.btn_scan = QPushButton("Start Scan")
        self.btn_scan.setStyleSheet(
            "background-color: #007acc; color: #fff; padding: 10px;"
            "font-size: 12pt; border-radius: 5px; margin: 5px;"
        )
        self.btn_scan.clicked.connect(self.start_scan)
        input_layout.addWidget(self.btn_scan)

        self.btn_reset = QPushButton("Reset")
        self.btn_reset.setStyleSheet(
            "background-color: #f44336; color: #fff; padding: 10px;"
            "font-size: 12pt; border-radius: 5px; margin: 5px;"
        )
        self.btn_reset.clicked.connect(self.reset_scanner)
        input_layout.addWidget(self.btn_reset)

        layout.addLayout(input_layout)

        # Output section
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setStyleSheet(
            "background-color: #fff; color: #000; padding: 10px; font-size: 12pt;"
        )
        layout.addWidget(self.output)

        # Total Devices Found Label
        self.total_devices_label = QLabel("Total Devices Found: 0")
        self.total_devices_label.setStyleSheet("font-size: 12pt; color: #000;")
        layout.addWidget(self.total_devices_label)

        self.setLayout(layout)

    def start_scan(self):
        network = self.input_network.text()
        if not network:
            show_error_message(self, "Please enter a valid network.")
            return

        try:
            # Validate the network
            ip_network = ipaddress.ip_network(network, strict=False)
        except ValueError as e:
            show_error_message(self, "Invalid network address.")
            return

        self.output.clear()
        self.devices_found.clear()
        self.total_devices_label.setText("Total Devices Found: 0")
        self.btn_scan.setEnabled(False)
        self.btn_reset.setEnabled(False)
        self.input_network.setEnabled(False)

        # Start scanning in a separate thread
        scanner = NetworkScanner(network)
        scanner.signals.device_found.connect(self.device_found)
        scanner.signals.scan_finished.connect(self.scan_finished)
        self.threadpool.start(scanner)

    def device_found(self, ip, mac, hostname):
        with self.lock:
            self.devices_found.append((ip, mac, hostname))
            self.output.append(f"IP: {ip}\tMAC: {mac}\tHostname: {hostname}")
            self.total_devices_label.setText(f"Total Devices Found: {len(self.devices_found)}")

    def scan_finished(self):
        self.output.append("Scan completed.")
        self.btn_scan.setEnabled(True)
        self.btn_reset.setEnabled(True)
        self.input_network.setEnabled(True)

    def reset_scanner(self):
        self.input_network.clear()
        self.output.clear()
        self.devices_found.clear()
        self.total_devices_label.setText("Total Devices Found: 0")

class WorkerSignals(QObject):
    device_found = pyqtSignal(str, str, str)  # IP, MAC, Hostname
    scan_finished = pyqtSignal()

class NetworkScanner(QRunnable):
    def __init__(self, network):
        super().__init__()
        self.network = network
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            # Create ARP request
            arp = ARP(pdst=self.network)
            ether = Ether(dst="ff:ff:ff:ff:ff:ff")
            packet = ether / arp

            # Send the packet and receive responses
            result = srp(packet, timeout=2, verbose=0)[0]

            for sent, received in result:
                ip = received.psrc
                mac = received.hwsrc
                # Resolve hostname
                try:
                    hostname = socket.gethostbyaddr(ip)[0]
                except:
                    hostname = "Unknown"
                self.signals.device_found.emit(ip, mac, hostname)

        except Exception as e:
            pass
        finally:
            self.signals.scan_finished.emit()
