# threads/network_diagram_thread.py

from PyQt6.QtCore import QThread, pyqtSignal
import ipaddress
import subprocess
import platform
import os
import networkx as nx
import matplotlib.pyplot as plt

class NetworkDiagramThread(QThread):
    output = pyqtSignal(str)
    finished = pyqtSignal(str)  # Emit the path to the generated diagram

    def __init__(self, network_range):
        super().__init__()
        self.network_range = network_range

    def run(self):
        self.output.emit("Starting network discovery...")
        try:
            network = ipaddress.IPv4Network(self.network_range, strict=False)
        except ValueError as e:
            self.output.emit(f"Invalid network range: {e}")
            self.finished.emit(None)
            return

        alive_hosts = []

        # Determine the ping command based on the OS
        if platform.system().lower() == "windows":
            ping_cmd = ["ping", "-n", "1", "-w", "100"]
        else:
            ping_cmd = ["ping", "-c", "1", "-W", "1"]

        # Ping all hosts in the network
        for ip in network.hosts():
            ip_str = str(ip)
            self.output.emit(f"Pinging {ip_str}...")
            try:
                response = subprocess.run(
                    ping_cmd + [ip_str],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                if response.returncode == 0:
                    self.output.emit(f"{ip_str} is alive.")
                    alive_hosts.append(ip_str)
                else:
                    self.output.emit(f"{ip_str} is unreachable.")
            except Exception as e:
                self.output.emit(f"Error pinging {ip_str}: {e}")

        if not alive_hosts:
            self.output.emit("No alive hosts found.")
            self.finished.emit(None)
            return

        self.output.emit("Creating network diagram...")

        # Create a network graph
        G = nx.Graph()

        # Add nodes
        for host in alive_hosts:
            G.add_node(host)

        # Simulate connections (for demonstration purposes)
        # In a real scenario, you would use more accurate methods to determine connections
        for i in range(len(alive_hosts) - 1):
            G.add_edge(alive_hosts[i], alive_hosts[i + 1])

        # Generate diagram
        try:
            plt.figure(figsize=(10, 8))
            pos = nx.spring_layout(G, k=0.5)
            nx.draw(
                G, pos, with_labels=True, node_color="#1f78b4", edge_color="#a6cee3", font_weight="bold"
            )
            diagram_path = os.path.join(os.getcwd(), "network_diagram.png")
            plt.savefig(diagram_path)
            plt.close()
            self.output.emit("Network diagram generated successfully.")
            self.finished.emit(diagram_path)
        except Exception as e:
            self.output.emit(f"Error generating diagram: {e}")
            self.finished.emit(None)
