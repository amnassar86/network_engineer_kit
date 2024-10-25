# threads/circuit_check_thread.py

from PyQt6.QtCore import QThread, pyqtSignal
import subprocess

class CircuitCheckThread(QThread):
    status_updated = pyqtSignal(int, str)  # circuit_id, status

    def __init__(self, ip_address, circuit_id):
        super().__init__()
        self.ip_address = ip_address
        self.circuit_id = circuit_id

    def run(self):
        try:
            # Ping the IP address
            response = subprocess.run(["ping", "-n", "1", "-w", "1000", self.ip_address],
                                      stdout=subprocess.DEVNULL)
            if response.returncode == 0:
                status = "Connected"
            else:
                status = "Disconnected"
        except Exception as e:
            status = "Error"

        # Emit the status
        self.status_updated.emit(self.circuit_id, status)
