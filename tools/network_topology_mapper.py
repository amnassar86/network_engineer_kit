# tools/network_topology_mapper.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QFrame, QLabel, QTextEdit, QHBoxLayout
)
from PyQt6.QtCore import Qt
from threads.topology_mapper_thread import TopologyMapperThread
from utils import show_error_message
import os
import networkx as nx
import matplotlib.pyplot as plt
import webbrowser

class NetworkTopologyMapper(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.is_mapping = False

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

        # Button layout
        button_layout = QHBoxLayout()
        self.btn_start_mapping = QPushButton("Start Mapping")
        self.btn_start_mapping.setStyleSheet(
            "background-color: #343b47; color: #fff; padding: 15px;"
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )
        self.btn_start_mapping.clicked.connect(self.toggle_mapping)
        button_layout.addWidget(self.btn_start_mapping)

        # Reset Button
        self.btn_reset = QPushButton("Reset")
        self.btn_reset.setStyleSheet(
            "background-color: #343b47; color: #fff; padding: 15px;"
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )
        self.btn_reset.clicked.connect(self.reset_topology_mapper)
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
        output_label = QLabel("Network Topology Mapping Results:")
        output_label.setStyleSheet("font-size: 12pt; color: #fff;")
        output_layout.addWidget(output_label)

        self.mapping_output = QTextEdit()
        self.mapping_output.setReadOnly(True)
        self.mapping_output.setStyleSheet(
            "background-color: #2c313c; color: #fff; padding: 10px; font-size: 12pt;"
        )
        output_layout.addWidget(self.mapping_output)

        # View Map Button
        self.btn_view_map = QPushButton("View Network Map")
        self.btn_view_map.setStyleSheet(
            "background-color: #007acc; color: #fff; padding: 15px;"
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )
        self.btn_view_map.clicked.connect(self.view_network_map)
        self.btn_view_map.setEnabled(False)
        output_layout.addWidget(self.btn_view_map)

        layout.addLayout(input_layout)
        layout.addLayout(output_layout)

        self.setLayout(layout)
        self.map_file = None

    def toggle_mapping(self):
        if not self.is_mapping:
            self.start_mapping()
        else:
            self.stop_mapping()

    def start_mapping(self):
        network_range = self.input_network_range.text()
        if not network_range:
            show_error_message(self, "Please enter a valid network range.")
            return

        self.mapping_output.clear()
        self.is_mapping = True
        self.btn_start_mapping.setText("Stop Mapping")
        self.btn_start_mapping.setStyleSheet(
            "background-color: red; color: #fff; padding: 15px;"
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )

        # Start the topology mapper thread
        self.mapper_thread = TopologyMapperThread(network_range)
        self.mapper_thread.output.connect(self.update_mapping_output)
        self.mapper_thread.finished.connect(self.mapping_finished)
        self.mapper_thread.start()

    def stop_mapping(self):
        if self.mapper_thread and self.mapper_thread.isRunning():
            self.mapper_thread.stop()
            self.mapper_thread.wait()
        self.mapping_finished(None)

    def update_mapping_output(self, text):
        self.mapping_output.append(text)

    def mapping_finished(self, graph_data):
        self.is_mapping = False
        self.btn_start_mapping.setText("Start Mapping")
        self.btn_start_mapping.setStyleSheet(
            "background-color: #343b47; color: #fff; padding: 15px;"
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )
        if graph_data:
            self.create_network_map(graph_data)
            self.btn_view_map.setEnabled(True)
        else:
            self.btn_view_map.setEnabled(False)

    def create_network_map(self, graph_data):
        try:
            G = nx.Graph()
            G.add_nodes_from(graph_data['nodes'])
            G.add_edges_from(graph_data['edges'])  # Edges are empty in this case

            self.map_file = os.path.join(os.getcwd(), 'network_map.png')
            plt.figure(figsize=(12, 8))
            pos = nx.spring_layout(G)
            labels = {node: data['label'] for node, data in G.nodes(data=True)}
            nx.draw(G, pos, with_labels=True, labels=labels, node_color='skyblue',
                    edge_color='gray', node_size=1500, font_size=10)
            plt.savefig(self.map_file)
            plt.close()
            self.mapping_output.append("Network map generated.")
        except Exception as e:
            show_error_message(self, f"Error creating network map: {e}")
            self.mapping_output.append(f"Error creating network map: {e}")
            self.map_file = None

    def view_network_map(self):
        if self.map_file and os.path.exists(self.map_file):
            webbrowser.open(self.map_file)
        else:
            show_error_message(self, "Network map file not found.")

    def reset_topology_mapper(self):
        self.input_network_range.clear()
        self.mapping_output.clear()
        self.map_file = None
        self.btn_view_map.setEnabled(False)
        if self.is_mapping:
            self.stop_mapping()
