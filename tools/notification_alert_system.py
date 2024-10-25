# tools/notification_alert_system.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QFrame, QLabel, QTextEdit, QHBoxLayout, QLineEdit, QSpinBox
)
from PyQt6.QtCore import Qt
from threads.notification_thread import NotificationThread
from utils import show_error_message

class NotificationAlertSystem(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.is_monitoring = False

    def init_ui(self):
        layout = QVBoxLayout()

        # Input section
        input_layout = QVBoxLayout()

        # Threshold input
        threshold_layout = QHBoxLayout()
        threshold_label = QLabel("CPU Usage Threshold (%):")
        threshold_label.setStyleSheet("font-size: 12pt; color: #fff;")
        self.threshold_input = QSpinBox()
        self.threshold_input.setRange(1, 100)
        self.threshold_input.setValue(80)
        self.threshold_input.setStyleSheet(
            "padding: 5px; font-size: 12pt; color: #fff; background-color: #2c313c;"
        )
        threshold_layout.addWidget(threshold_label)
        threshold_layout.addWidget(self.threshold_input)
        input_layout.addLayout(threshold_layout)

        # Email input
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter Email for Alerts")
        self.email_input.setStyleSheet(
            "padding: 10px; font-size: 12pt; color: #fff; background-color: #2c313c; border: none;"
        )
        input_layout.addWidget(self.email_input)

        # Button layout
        button_layout = QHBoxLayout()
        self.btn_start_monitoring = QPushButton("Start Monitoring")
        self.btn_start_monitoring.setStyleSheet(
            "background-color: #343b47; color: #fff; padding: 15px;"
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )
        self.btn_start_monitoring.clicked.connect(self.toggle_monitoring)
        button_layout.addWidget(self.btn_start_monitoring)

        # Reset Button
        self.btn_reset = QPushButton("Reset")
        self.btn_reset.setStyleSheet(
            "background-color: #343b47; color: #fff; padding: 15px;"
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )
        self.btn_reset.clicked.connect(self.reset_notification_system)
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
        output_label = QLabel("Alerts:")
        output_label.setStyleSheet("font-size: 12pt; color: #fff;")
        output_layout.addWidget(output_label)

        self.alert_output = QTextEdit()
        self.alert_output.setReadOnly(True)
        self.alert_output.setStyleSheet(
            "background-color: #2c313c; color: #fff; padding: 10px; font-size: 12pt;"
        )
        output_layout.addWidget(self.alert_output)

        layout.addLayout(input_layout)
        layout.addLayout(output_layout)

        self.setLayout(layout)

    def toggle_monitoring(self):
        if not self.is_monitoring:
            self.start_monitoring()
        else:
            self.stop_monitoring()

    def start_monitoring(self):
        threshold = self.threshold_input.value()
        email = self.email_input.text()
        if not email:
            show_error_message(self, "Please enter a valid email address.")
            return

        self.alert_output.clear()
        self.is_monitoring = True
        self.btn_start_monitoring.setText("Stop Monitoring")
        self.btn_start_monitoring.setStyleSheet(
            "background-color: red; color: #fff; padding: 15px;"
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )

        # Start the notification thread
        self.notification_thread = NotificationThread(threshold, email)
        self.notification_thread.output.connect(self.update_alert_output)
        self.notification_thread.finished.connect(self.monitoring_finished)
        self.notification_thread.start()

    def stop_monitoring(self):
        if self.notification_thread and self.notification_thread.isRunning():
            self.notification_thread.stop()
            self.notification_thread.wait()
        self.monitoring_finished()

    def update_alert_output(self, text):
        self.alert_output.append(text)

    def monitoring_finished(self):
        self.is_monitoring = False
        self.btn_start_monitoring.setText("Start Monitoring")
        self.btn_start_monitoring.setStyleSheet(
            "background-color: #343b47; color: #fff; padding: 15px;"
            "font-size: 12pt; border-radius: 8px; margin: 5px;"
        )

    def reset_notification_system(self):
        self.email_input.clear()
        self.threshold_input.setValue(80)
        self.alert_output.clear()
        if self.is_monitoring:
            self.stop_monitoring()
