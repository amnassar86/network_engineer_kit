# threads/traceroute_worker.py

from PyQt6.QtCore import QThread, pyqtSignal
import subprocess

class TracerouteWorker(QThread):
    result = pyqtSignal(str, str)  # ip_address, output

    def __init__(self, ip_address):
        super().__init__()
        self.ip_address = ip_address

    def run(self):
        try:
            output = subprocess.check_output(["tracert", "-d", self.ip_address],
                                             stderr=subprocess.STDOUT, universal_newlines=True)
            self.result.emit(self.ip_address, output)
        except Exception as e:
            self.result.emit(self.ip_address, f"An error occurred:\n{e}")
