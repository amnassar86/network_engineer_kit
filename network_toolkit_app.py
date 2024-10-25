# network_toolkit_app.py

from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QLabel, QPushButton, QWidget, QStatusBar,
    QTabWidget, QHBoxLayout, QFrame, QSizePolicy, QSpacerItem, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Import tool widgets
from tools.ping_tool import PingTool
from tools.traceroute_tool import TracerouteTool
from tools.ip_scanner_tool import IPScannerTool
from tools.subnet_calculator_tool import SubnetCalculatorTool
from tools.arp_tool import ARPTool
from tools.bandwidth_monitor_tool import BandwidthMonitorTool
from tools.network_diagram_tool import NetworkDiagramTool
from tools.dns_lookup_tool import DNSLookupTool
from tools.network_interface_tool import NetworkInterfaceTool
from tools.syslog_viewer_tool import SyslogViewerTool
from tools.snmp_manager_tool import SNMPManagerTool

from tools.latency_jitter_tool import LatencyJitterTool
from tools.netstat_viewer_tool import NetstatViewerTool
from tools.wifi_analyzer_tool import WifiAnalyzerTool

from tools.port_forwarding_tester import PortForwardingTester
from tools.network_performance_tester import NetworkPerformanceTester

from tools.packet_sniffer_tool import PacketSnifferTool
from tools.network_topology_mapper import NetworkTopologyMapper
from tools.network_security_scanner import NetworkSecurityScanner
from tools.circuit_checker_tool import CircuitCheckerTool








class NetworkToolkitApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Network Engineer Toolkit")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: #1f232a; color: #fff;")

        # Central widget and main layout
        central_widget = QWidget(self)
        main_layout = QHBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        # Status Bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Ready")

        # Sidebar
        self.create_sidebar()

        # Content area
        self.create_content_area()

        # Main layout arrangement
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content_area)

    def create_sidebar(self):
        # Sidebar widget and layout
        self.sidebar = QFrame()
        self.sidebar.setStyleSheet("background-color: #2c313c;")
        self.sidebar.setFixedWidth(220)  # Adjusted width to accommodate tool names

        # Scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background-color: #2c313c; border: none;")
        scroll_content = QWidget()
        sidebar_layout = QVBoxLayout(scroll_content)
        sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Title
        title = QLabel("Tools")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("padding: 20px; color: #fff;")
        sidebar_layout.addWidget(title)

        # Tool buttons
        self.tool_buttons = {}

        tool_info = [
            ("Ping Tool", self.switch_to_ping_tool),
            ("Traceroute Tool", self.switch_to_traceroute_tool),
            ("IP Scanner", self.switch_to_ip_scanner_tool),
            ("Subnet Calculator", self.switch_to_subnet_calculator_tool),
            ("ARP Tool", self.switch_to_arp_tool),
            ("Bandwidth Monitor", self.switch_to_bandwidth_monitor_tool),
            ("Network Diagram Generator", self.switch_to_network_diagram_tool),
            ("DNS Lookup Tool", self.switch_to_dns_lookup_tool),
            ("Network Interface Analyzer", self.switch_to_network_interface_tool),
            ("Syslog Viewer", self.switch_to_syslog_viewer_tool),
            ("SNMP Manager", self.switch_to_snmp_manager_tool),
            ("Latency and Jitter Monitor", self.switch_to_latency_jitter_tool),
            ("Netstat Viewer", self.switch_to_netstat_viewer_tool),
            ("Wi-Fi Analyzer", self.switch_to_wifi_analyzer_tool),
            ("Port Forwarding Tester", self.switch_to_port_forwarding_tester),
            ("Network Performance Tester", self.switch_to_network_performance_tester),
            ("Packet Sniffer/Analyzer", self.switch_to_packet_sniffer_tool),
            ("Network Topology Mapper", self.switch_to_network_topology_mapper),
            ("Network Security Scanner", self.switch_to_network_security_scanner),
            ("Circuit Connection Checker", self.switch_to_circuit_checker_tool),

            # Add more tools here as needed
        ]

        button_style = """
        QPushButton {
            background-color: #343b47;
            color: #fff;
            padding: 10px;
            font-size: 11pt;  /* Adjusted font size */
            border: none;
            text-align: left;
        }
        QPushButton:hover {
            background-color: #3e4452;
        }
        """

        for name, handler in tool_info:
            btn = QPushButton(name)
            btn.setStyleSheet(button_style)
            btn.setFixedHeight(50)
            btn.clicked.connect(handler)
            sidebar_layout.addWidget(btn)
            self.tool_buttons[name] = btn

        # Spacer to push buttons to the top
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sidebar_layout.addItem(spacer)

        scroll_area.setWidget(scroll_content)

        # Set the scroll area as the sidebar's layout
        sidebar_layout_container = QVBoxLayout(self.sidebar)
        sidebar_layout_container.setContentsMargins(0, 0, 0, 0)
        sidebar_layout_container.addWidget(scroll_area)

    def create_content_area(self):
        # Content area to hold tabs
        self.content_area = QWidget()
        content_layout = QVBoxLayout()
        self.content_area.setLayout(content_layout)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.tabBar().setVisible(False)  # Hide tab headers
        content_layout.addWidget(self.tabs)

        # Create tabs for each tool
        self.ping_tool = PingTool()
        self.traceroute_tool = TracerouteTool()
        self.ip_scanner_tool = IPScannerTool()
        self.subnet_calculator_tool = SubnetCalculatorTool()
        self.arp_tool = ARPTool()
        self.bandwidth_monitor_tool = BandwidthMonitorTool()
        self.network_diagram_tool = NetworkDiagramTool()
        self.dns_lookup_tool = DNSLookupTool()
        self.network_interface_tool = NetworkInterfaceTool()
        self.syslog_viewer_tool = SyslogViewerTool()
        self.snmp_manager_tool = SNMPManagerTool()
        self.latency_jitter_tool = LatencyJitterTool()
        self.netstat_viewer_tool = NetstatViewerTool()
        self.wifi_analyzer_tool = WifiAnalyzerTool()
        # Add more tool instances here as needed

        self.tabs.addTab(self.ping_tool, "Ping Tool")
        self.tabs.addTab(self.traceroute_tool, "Traceroute Tool")
        self.tabs.addTab(self.ip_scanner_tool, "IP Scanner")
        self.tabs.addTab(self.subnet_calculator_tool, "Subnet Calculator")
        self.tabs.addTab(self.arp_tool, "ARP Tool")
        self.tabs.addTab(self.bandwidth_monitor_tool, "Bandwidth Monitor")
        self.tabs.addTab(self.network_diagram_tool, "Network Diagram Generator")
        self.tabs.addTab(self.dns_lookup_tool, "DNS Lookup Tool")
        self.tabs.addTab(self.network_interface_tool, "Network Interface Analyzer")
        self.tabs.addTab(self.syslog_viewer_tool, "Syslog Viewer")
        self.tabs.addTab(self.snmp_manager_tool, "SNMP Manager")
        self.tabs.addTab(self.latency_jitter_tool, "Latency and Jitter Monitor")
        self.tabs.addTab(self.netstat_viewer_tool, "Netstat Viewer")
        self.tabs.addTab(self.wifi_analyzer_tool, "Wi-Fi Analyzer")
        self.port_forwarding_tester = PortForwardingTester()
        self.tabs.addTab(self.port_forwarding_tester, "Port Forwarding Tester")
        self.network_performance_tester = NetworkPerformanceTester()
        self.tabs.addTab(self.network_performance_tester, "Network Performance Tester")
        self.packet_sniffer_tool = PacketSnifferTool()
        self.tabs.addTab(self.packet_sniffer_tool, "Packet Sniffer/Analyzer")
        self.network_topology_mapper = NetworkTopologyMapper()
        self.tabs.addTab(self.network_topology_mapper, "Network Topology Mapper")
        self.network_security_scanner = NetworkSecurityScanner()
        self.tabs.addTab(self.network_security_scanner, "Network Security Scanner")
        self.circuit_checker_tool = CircuitCheckerTool()
        self.tabs.addTab(self.circuit_checker_tool, "Circuit Connection Checker")

        # Add more tabs here as needed

        # Initialize by selecting the first tool
        self.switch_to_ping_tool()

    def reset_button_styles(self):
        # Reset styles for all buttons
        for btn in self.tool_buttons.values():
            btn.setStyleSheet("""
            QPushButton {
                background-color: #343b47;
                color: #fff;
                padding: 10px;
                font-size: 11pt;
                border: none;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #3e4452;
            }
            """)

    def highlight_button(self, button_name):
        # Highlight the selected button
        self.reset_button_styles()
        btn = self.tool_buttons.get(button_name)
        if btn:
            btn.setStyleSheet("""
            QPushButton {
                background-color: #007acc;
                color: #fff;
                padding: 10px;
                font-size: 11pt;
                border: none;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #007acc;
            }
            """)

    # Methods to switch tabs and highlight the active button
    def switch_to_ping_tool(self):
        self.tabs.setCurrentWidget(self.ping_tool)
        self.highlight_button("Ping Tool")
        self.status.showMessage("Ping Tool selected")

    def switch_to_traceroute_tool(self):
        self.tabs.setCurrentWidget(self.traceroute_tool)
        self.highlight_button("Traceroute Tool")
        self.status.showMessage("Traceroute Tool selected")

    def switch_to_ip_scanner_tool(self):
        self.tabs.setCurrentWidget(self.ip_scanner_tool)
        self.highlight_button("IP Scanner")
        self.status.showMessage("IP Scanner selected")

    def switch_to_subnet_calculator_tool(self):
        self.tabs.setCurrentWidget(self.subnet_calculator_tool)
        self.highlight_button("Subnet Calculator")
        self.status.showMessage("Subnet Calculator selected")

    def switch_to_arp_tool(self):
        self.tabs.setCurrentWidget(self.arp_tool)
        self.highlight_button("ARP Tool")
        self.status.showMessage("ARP Tool selected")

    def switch_to_bandwidth_monitor_tool(self):
        self.tabs.setCurrentWidget(self.bandwidth_monitor_tool)
        self.highlight_button("Bandwidth Monitor")
        self.status.showMessage("Bandwidth Monitor selected")

    def switch_to_network_diagram_tool(self):
        self.tabs.setCurrentWidget(self.network_diagram_tool)
        self.highlight_button("Network Diagram Generator")
        self.status.showMessage("Network Diagram Generator selected")

    def switch_to_dns_lookup_tool(self):
        self.tabs.setCurrentWidget(self.dns_lookup_tool)
        self.highlight_button("DNS Lookup Tool")
        self.status.showMessage("DNS Lookup Tool selected")

    def switch_to_network_interface_tool(self):
        self.tabs.setCurrentWidget(self.network_interface_tool)
        self.highlight_button("Network Interface Analyzer")
        self.status.showMessage("Network Interface Analyzer selected")

    def switch_to_syslog_viewer_tool(self):
        self.tabs.setCurrentWidget(self.syslog_viewer_tool)
        self.highlight_button("Syslog Viewer")
        self.status.showMessage("Syslog Viewer selected")

    def switch_to_snmp_manager_tool(self):
        self.tabs.setCurrentWidget(self.snmp_manager_tool)
        self.highlight_button("SNMP Manager")
        self.status.showMessage("SNMP Manager selected")

    def switch_to_latency_jitter_tool(self):
        self.tabs.setCurrentWidget(self.latency_jitter_tool)
        self.highlight_button("Latency and Jitter Monitor")
        self.status.showMessage("Latency and Jitter Monitor selected")

    def switch_to_netstat_viewer_tool(self):
        self.tabs.setCurrentWidget(self.netstat_viewer_tool)
        self.highlight_button("Netstat Viewer")
        self.status.showMessage("Netstat Viewer selected")

    def switch_to_wifi_analyzer_tool(self):
        self.tabs.setCurrentWidget(self.wifi_analyzer_tool)
        self.highlight_button("Wi-Fi Analyzer")
        self.status.showMessage("Wi-Fi Analyzer selected")

    def switch_to_port_forwarding_tester(self):
        self.tabs.setCurrentWidget(self.port_forwarding_tester)
        self.highlight_button("Port Forwarding Tester")
        self.status.showMessage("Port Forwarding Tester selected")

    def switch_to_network_performance_tester(self):
        self.tabs.setCurrentWidget(self.network_performance_tester)
        self.highlight_button("Network Performance Tester")
        self.status.showMessage("Network Performance Tester selected")

    def switch_to_packet_sniffer_tool(self):
        self.tabs.setCurrentWidget(self.packet_sniffer_tool)
        self.highlight_button("Packet Sniffer/Analyzer")
        self.status.showMessage("Packet Sniffer/Analyzer selected")

    def switch_to_network_topology_mapper(self):
        self.tabs.setCurrentWidget(self.network_topology_mapper)
        self.highlight_button("Network Topology Mapper")
        self.status.showMessage("Network Topology Mapper selected")

    def switch_to_network_security_scanner(self):
        self.tabs.setCurrentWidget(self.network_security_scanner)
        self.highlight_button("Network Security Scanner")
        self.status.showMessage("Network Security Scanner selected")

    def switch_to_circuit_checker_tool(self):
        self.tabs.setCurrentWidget(self.circuit_checker_tool)
        self.highlight_button("Circuit Connection Checker")
        self.status.showMessage("Circuit Connection Checker selected")

    # Add more switch methods for new tools as needed
