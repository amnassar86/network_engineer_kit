# tools/subnet_calculator_tool.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTextEdit, QLabel, QComboBox, QFormLayout
)
from PyQt6.QtCore import Qt
import ipaddress

class SubnetCalculatorTool(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Input form
        form_layout = QFormLayout()

        self.input_network = QLineEdit()
        self.input_network.setPlaceholderText("e.g., 192.168.1.0/24 or 192.168.1.0")
        form_layout.addRow("Network Address:", self.input_network)

        self.input_subnets = QLineEdit()
        self.input_subnets.setPlaceholderText("Number of Subnets (for Subnetting)")
        form_layout.addRow("Number of Subnets:", self.input_subnets)

        self.input_hosts = QLineEdit()
        self.input_hosts.setPlaceholderText("Number of Hosts per Subnet")
        form_layout.addRow("Hosts per Subnet:", self.input_hosts)

        self.input_vlans = QLineEdit()
        self.input_vlans.setPlaceholderText("VLAN IDs (comma-separated)")
        form_layout.addRow("VLAN IDs:", self.input_vlans)

        self.calc_type = QComboBox()
        self.calc_type.addItems(["CIDR Calculation", "Subnetting", "Supernetting", "VLAN Calculation"])
        form_layout.addRow("Calculation Type:", self.calc_type)

        layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()
        self.btn_calculate = QPushButton("Calculate")
        self.btn_calculate.clicked.connect(self.calculate)
        button_layout.addWidget(self.btn_calculate)

        self.btn_reset = QPushButton("Reset")
        self.btn_reset.clicked.connect(self.reset)
        button_layout.addWidget(self.btn_reset)

        layout.addLayout(button_layout)

        # Output
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        self.setLayout(layout)

    def calculate(self):
        calc_type = self.calc_type.currentText()
        network_input = self.input_network.text()
        try:
            if calc_type == "CIDR Calculation":
                self.calculate_cidr(network_input)
            elif calc_type == "Subnetting":
                self.calculate_subnetting(network_input)
            elif calc_type == "Supernetting":
                self.calculate_supernetting(network_input)
            elif calc_type == "VLAN Calculation":
                self.calculate_vlan(network_input)
            else:
                self.output.setText("Invalid calculation type.")
        except Exception as e:
            self.output.setText(f"Error: {e}")

    def calculate_cidr(self, network_input):
        network = ipaddress.ip_network(network_input, strict=False)
        self.output.setText(f"Network: {network}")
        self.output.append(f"Network Address: {network.network_address}")
        self.output.append(f"Broadcast Address: {network.broadcast_address}")
        self.output.append(f"Subnet Mask: {network.netmask}")
        self.output.append(f"Wildcard Mask: {network.hostmask}")
        self.output.append(f"Number of Hosts: {network.num_addresses - 2}")
        self.output.append(f"Usable Hosts Range: {list(network.hosts())[0]} - {list(network.hosts())[-1]}")

    def calculate_subnetting(self, network_input):
        num_subnets = self.input_subnets.text()
        hosts_per_subnet = self.input_hosts.text()

        if not num_subnets and not hosts_per_subnet:
            self.output.setText("Please enter the number of subnets or hosts per subnet.")
            return

        network = ipaddress.ip_network(network_input, strict=False)

        if num_subnets:
            num_subnets = int(num_subnets)
            new_prefix = network.prefixlen + (num_subnets - 1).bit_length()
            subnets = list(network.subnets(new_prefix=new_prefix))
        elif hosts_per_subnet:
            hosts_per_subnet = int(hosts_per_subnet)
            new_prefix = 32 - (hosts_per_subnet + 2 - 1).bit_length()
            subnets = list(network.subnets(new_prefix=new_prefix))
        else:
            self.output.setText("Invalid input for subnetting.")
            return

        self.output.setText(f"Original Network: {network}")
        self.output.append(f"Subnet Mask: {network.netmask}")
        self.output.append(f"Number of Subnets: {len(subnets)}")
        self.output.append("Subnets:")
        for subnet in subnets:
            self.output.append(f"{subnet}")

    def calculate_supernetting(self, network_input):
        # Accept multiple networks separated by commas
        networks = [ipaddress.ip_network(n.strip(), strict=False) for n in network_input.split(',')]
        supernet = ipaddress.collapse_addresses(networks)
        supernet_list = list(supernet)
        if len(supernet_list) == 1:
            supernet = supernet_list[0]
            self.output.setText(f"Supernet: {supernet}")
            self.output.append(f"Network Address: {supernet.network_address}")
            self.output.append(f"Broadcast Address: {supernet.broadcast_address}")
            self.output.append(f"Subnet Mask: {supernet.netmask}")
            self.output.append(f"Number of Hosts: {supernet.num_addresses - 2}")
        else:
            self.output.setText("Unable to create a single supernet from the provided networks.")

    def calculate_vlan(self, network_input):
        vlan_ids = self.input_vlans.text()
        if not vlan_ids:
            self.output.setText("Please enter VLAN IDs.")
            return

        vlan_ids = [v.strip() for v in vlan_ids.split(',')]
        network = ipaddress.ip_network(network_input, strict=False)
        hosts = list(network.hosts())

        if len(hosts) < len(vlan_ids):
            self.output.setText("Not enough hosts in the network for the given VLAN IDs.")
            return

        vlan_subnets = {}
        hosts_per_vlan = len(hosts) // len(vlan_ids)

        for index, vlan_id in enumerate(vlan_ids):
            start = index * hosts_per_vlan
            end = start + hosts_per_vlan
            vlan_hosts = hosts[start:end]
            vlan_subnets[vlan_id] = vlan_hosts

        self.output.setText("VLAN Assignments:")
        for vlan_id, vlan_hosts in vlan_subnets.items():
            self.output.append(f"VLAN {vlan_id}:")
            self.output.append(f"Hosts: {vlan_hosts[0]} - {vlan_hosts[-1]}")
            self.output.append("-" * 30)

    def reset(self):
        self.input_network.clear()
        self.input_subnets.clear()
        self.input_hosts.clear()
        self.input_vlans.clear()
        self.output.clear()
