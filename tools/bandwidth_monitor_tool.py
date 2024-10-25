# tools/bandwidth_monitor_tool.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFrame, QLabel, QTextEdit, QHBoxLayout
from PyQt6.QtCore import Qt
from threads.bandwidth_monitor_thread import BandwidthMonitorThread

class BandwidthMonitorTool(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.is_monitoring = False

    def init_ui(self):
        layout = QVBoxLayout()

        # Input section
        input_layout = QVBoxLayout()

        # Button layout
        button_layout = QHBoxLayout()
        self.btn_start_bandwidth = QPushButton("Start Bandwidth Monitor")
        self.btn_start_bandwidth.setStyleSheet(
            "background-color: #343b47; color: #fff; padding: 15px; "
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )
        self.btn_start_bandwidth.clicked.connect(self.toggle_bandwidth_monitor)
        button_layout.addWidget(self.btn_start_bandwidth)

        # Reset Button
        self.btn_reset = QPushButton("Reset")
        self.btn_reset.setStyleSheet(
            "background-color: #343b47; color: #fff; padding: 15px; "
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )
        self.btn_reset.clicked.connect(self.reset_bandwidth_monitor_tool)
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
        output_label = QLabel("Bandwidth Monitor Results:")
        output_label.setStyleSheet("font-size: 12pt; color: #fff;")
        output_layout.addWidget(output_label)

        self.bandwidth_output = QTextEdit()
        self.bandwidth_output.setReadOnly(True)
        self.bandwidth_output.setStyleSheet(
            "background-color: #2c313c; color: #fff; padding: 10px; font-size: 12pt;")
        output_layout.addWidget(self.bandwidth_output)

        layout.addLayout(input_layout)
        layout.addLayout(output_layout)

        self.setLayout(layout)

    def toggle_bandwidth_monitor(self):
        if not self.is_monitoring:
            self.execute_bandwidth_monitor()
        else:
            self.stop_bandwidth_monitor()

    def execute_bandwidth_monitor(self):
        self.bandwidth_output.clear()
        self.btn_start_bandwidth.setText("Stop Bandwidth Monitor")
        self.btn_start_bandwidth.setStyleSheet(
            "background-color: red; color: #fff; padding: 15px; "
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )
        self.is_monitoring = True

        self.bandwidth_thread = BandwidthMonitorThread()
        self.bandwidth_thread.output.connect(self.update_bandwidth_output)
        self.bandwidth_thread.finished.connect(self.bandwidth_monitor_finished)
        self.bandwidth_thread.start()

    def stop_bandwidth_monitor(self):
        if self.bandwidth_thread and self.bandwidth_thread.isRunning():
            self.bandwidth_thread.stop()
            self.bandwidth_thread.wait()
        self.bandwidth_monitor_finished()

    def bandwidth_monitor_finished(self, avg_download=None, avg_upload=None):
        self.is_monitoring = False
        self.btn_start_bandwidth.setText("Start Bandwidth Monitor")
        self.btn_start_bandwidth.setStyleSheet(
            "background-color: #343b47; color: #fff; padding: 15px; "
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )
        if avg_download and avg_upload:
            avg_result = f"\nAverage Download Speed: {avg_download:.2f} Mbps\n" \
                         f"Average Upload Speed: {avg_upload:.2f} Mbps"
            self.bandwidth_output.append(avg_result)

    def update_bandwidth_output(self, text):
        self.bandwidth_output.append(text)

    def reset_bandwidth_monitor_tool(self):
        self.bandwidth_output.clear()
        if self.is_monitoring:
            self.stop_bandwidth_monitor()
