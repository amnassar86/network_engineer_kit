# threads/port_check_thread.py

from PyQt6.QtCore import QThread, pyqtSignal
import socket
import time

class PortCheckThread(QThread):
    output = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, target, port):
        super().__init__()
        self.target = target
        self.port = port
        self._is_running = True

    def run(self):
        try:
            self.output.emit(f"Checking port {self.port} on {self.target}...")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(5)
                result = sock.connect_ex((self.target, self.port))
                if result == 0:
                    self.output.emit(f"Port {self.port} is open on {self.target}.")
                else:
                    self.output.emit(f"Port {self.port} is closed or unreachable on {self.target}.")
        except Exception as e:
            self.output.emit(f"Error: {e}")
        finally:
            self.finished.emit()

    def stop(self):
        self._is_running = False
