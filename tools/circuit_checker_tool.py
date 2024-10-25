# tools/circuit_checker_tool.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QLabel, QMessageBox, QHeaderView, QAbstractItemView, QDialog,
    QTextEdit, QFormLayout, QWidget
)
from PyQt6.QtCore import Qt, QTimer
from threads.circuit_check_thread import CircuitCheckThread
from threads.traceroute_worker import TracerouteWorker
from database import get_connection

class CircuitCheckerTool(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_circuits()
        self.setup_timer()
        self.threads = []  # Store references to threads

    def init_ui(self):
        layout = QVBoxLayout()

        # Form for adding a new circuit
        form_layout = QHBoxLayout()

        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText("Circuit Name")
        self.input_name.setStyleSheet("padding: 5px;")
        form_layout.addWidget(self.input_name)

        self.input_number = QLineEdit()
        self.input_number.setPlaceholderText("Circuit Number")
        self.input_number.setStyleSheet("padding: 5px;")
        form_layout.addWidget(self.input_number)

        self.input_location = QLineEdit()
        self.input_location.setPlaceholderText("Location")
        self.input_location.setStyleSheet("padding: 5px;")
        form_layout.addWidget(self.input_location)

        self.input_ip = QLineEdit()
        self.input_ip.setPlaceholderText("IP Address")
        self.input_ip.setStyleSheet("padding: 5px;")
        form_layout.addWidget(self.input_ip)

        self.btn_add_circuit = QPushButton("Add Circuit")
        self.btn_add_circuit.clicked.connect(self.add_circuit)
        form_layout.addWidget(self.btn_add_circuit)

        layout.addLayout(form_layout)

        # Table to display circuits
        self.circuit_table = QTableWidget()
        self.circuit_table.setColumnCount(7)
        self.circuit_table.setHorizontalHeaderLabels([
            "ID", "Name", "Number", "Location", "IP Address", "Status", "Actions"
        ])
        self.circuit_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.circuit_table.horizontalHeader().setStretchLastSection(False)
        self.circuit_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.circuit_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        layout.addWidget(self.circuit_table)

        # Adjust column widths
        self.circuit_table.setColumnWidth(0, 50)   # ID
        self.circuit_table.setColumnWidth(1, 150)  # Name
        self.circuit_table.setColumnWidth(2, 100)  # Number
        self.circuit_table.setColumnWidth(3, 150)  # Location
        self.circuit_table.setColumnWidth(4, 120)  # IP Address
        self.circuit_table.setColumnWidth(5, 100)  # Status
        self.circuit_table.setColumnWidth(6, 300)  # Actions

        self.setLayout(layout)

    def load_circuits(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM circuits")
        rows = cursor.fetchall()
        conn.close()

        self.circuit_table.setRowCount(0)
        for row in rows:
            self.add_table_row(row)

    def add_table_row(self, row_data):
        row_position = self.circuit_table.rowCount()
        self.circuit_table.insertRow(row_position)

        for i, data in enumerate(row_data):
            item = QTableWidgetItem(str(data))
            self.circuit_table.setItem(row_position, i, item)

        # Actions: Edit, Delete, Traceroute Buttons
        actions_layout = QHBoxLayout()
        actions_layout.setContentsMargins(0, 0, 0, 0)
        actions_layout.setSpacing(5)

        edit_button = QPushButton("Edit")
        edit_button.setFixedWidth(80)
        edit_button.clicked.connect(lambda _, row=row_position: self.edit_circuit(row))
        actions_layout.addWidget(edit_button)

        delete_button = QPushButton("Delete")
        delete_button.setFixedWidth(80)
        delete_button.clicked.connect(lambda _, row=row_position: self.delete_circuit(row))
        actions_layout.addWidget(delete_button)

        traceroute_button = QPushButton("Traceroute")
        traceroute_button.setFixedWidth(100)
        ip_address = row_data[4]
        traceroute_button.clicked.connect(lambda _, ip=ip_address: self.perform_traceroute(ip))
        actions_layout.addWidget(traceroute_button)

        actions_widget = QWidget()
        actions_widget.setLayout(actions_layout)
        self.circuit_table.setCellWidget(row_position, 6, actions_widget)

        # Resize the "Actions" column to fit the content
        self.circuit_table.resizeColumnToContents(6)

    def add_circuit(self):
        name = self.input_name.text()
        number = self.input_number.text()
        location = self.input_location.text()
        ip_address = self.input_ip.text()
        status = "Unknown"

        if not all([name, number, location, ip_address]):
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO circuits (name, number, location, ip_address, status)
            VALUES (?, ?, ?, ?, ?)
        """, (name, number, location, ip_address, status))
        conn.commit()
        circuit_id = cursor.lastrowid
        conn.close()

        self.input_name.clear()
        self.input_number.clear()
        self.input_location.clear()
        self.input_ip.clear()

        self.add_table_row((circuit_id, name, number, location, ip_address, status))

        # Trigger immediate status check
        thread = CircuitCheckThread(ip_address, circuit_id)
        thread.status_updated.connect(self.update_circuit_status)
        thread.finished.connect(lambda: self.remove_thread(thread))
        self.threads.append(thread)
        thread.start()

    def setup_timer(self):
        # Set up a timer to periodically check the circuit statuses
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_all_circuits)
        self.timer.start(60000)  # Check every 60 seconds

    def check_all_circuits(self):
        row_count = self.circuit_table.rowCount()
        for row in range(row_count):
            ip_address = self.circuit_table.item(row, 4).text()
            circuit_id = int(self.circuit_table.item(row, 0).text())
            # Start a thread to check each circuit
            thread = CircuitCheckThread(ip_address, circuit_id)
            thread.status_updated.connect(self.update_circuit_status)
            thread.finished.connect(lambda: self.remove_thread(thread))
            self.threads.append(thread)
            thread.start()

    def remove_thread(self, thread):
        if thread in self.threads:
            self.threads.remove(thread)

    def update_circuit_status(self, circuit_id, status):
        # Update the status in the database and table
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE circuits SET status = ? WHERE id = ?", (status, circuit_id))
        conn.commit()
        conn.close()

        # Update the status in the table
        row_count = self.circuit_table.rowCount()
        for row in range(row_count):
            if int(self.circuit_table.item(row, 0).text()) == circuit_id:
                self.circuit_table.setItem(row, 5, QTableWidgetItem(status))
                break

    def perform_traceroute(self, ip_address):
        # Start the traceroute in a separate thread
        traceroute_thread = TracerouteWorker(ip_address)
        traceroute_thread.result.connect(self.display_traceroute_result)
        traceroute_thread.finished.connect(lambda: self.remove_thread(traceroute_thread))
        self.threads.append(traceroute_thread)
        traceroute_thread.start()

    def display_traceroute_result(self, ip_address, output):
        # Display the output in a dialog
        traceroute_output = QTextEdit()
        traceroute_output.setPlainText(output)
        traceroute_output.setReadOnly(True)
        traceroute_output.setMinimumSize(600, 400)

        dialog = QDialog(self)
        dialog.setWindowTitle(f"Traceroute to {ip_address}")
        layout = QVBoxLayout(dialog)
        layout.addWidget(traceroute_output)
        dialog.setLayout(layout)
        dialog.exec()

    def edit_circuit(self, row):
        # Retrieve current circuit data
        circuit_id = int(self.circuit_table.item(row, 0).text())
        name = self.circuit_table.item(row, 1).text()
        number = self.circuit_table.item(row, 2).text()
        location = self.circuit_table.item(row, 3).text()
        ip_address = self.circuit_table.item(row, 4).text()

        # Create a dialog to edit the circuit
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Circuit")
        layout = QFormLayout(dialog)

        input_name = QLineEdit(name)
        input_number = QLineEdit(number)
        input_location = QLineEdit(location)
        input_ip = QLineEdit(ip_address)

        layout.addRow("Circuit Name:", input_name)
        layout.addRow("Circuit Number:", input_number)
        layout.addRow("Location:", input_location)
        layout.addRow("IP Address:", input_ip)

        btn_save = QPushButton("Save")
        btn_save.clicked.connect(lambda: self.save_circuit_changes(dialog, circuit_id, row, input_name.text(), input_number.text(), input_location.text(), input_ip.text()))
        layout.addWidget(btn_save)

        dialog.setLayout(layout)
        dialog.exec()

    def save_circuit_changes(self, dialog, circuit_id, row, name, number, location, ip_address):
        if not all([name, number, location, ip_address]):
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
            return

        # Update the database
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE circuits SET name = ?, number = ?, location = ?, ip_address = ? WHERE id = ?
        """, (name, number, location, ip_address, circuit_id))
        conn.commit()
        conn.close()

        # Update the table
        self.circuit_table.setItem(row, 1, QTableWidgetItem(name))
        self.circuit_table.setItem(row, 2, QTableWidgetItem(number))
        self.circuit_table.setItem(row, 3, QTableWidgetItem(location))
        self.circuit_table.setItem(row, 4, QTableWidgetItem(ip_address))

        dialog.accept()

        # Optionally, re-check the status after editing
        thread = CircuitCheckThread(ip_address, circuit_id)
        thread.status_updated.connect(self.update_circuit_status)
        thread.finished.connect(lambda: self.remove_thread(thread))
        self.threads.append(thread)
        thread.start()

    def delete_circuit(self, row):
        circuit_id = int(self.circuit_table.item(row, 0).text())
        response = QMessageBox.question(self, "Delete Circuit", "Are you sure you want to delete this circuit?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if response == QMessageBox.StandardButton.Yes:
            # Remove from database
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM circuits WHERE id = ?", (circuit_id,))
            conn.commit()
            conn.close()

            # Remove from table
            self.circuit_table.removeRow(row)
