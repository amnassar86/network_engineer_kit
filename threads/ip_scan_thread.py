# threads/ip_scan_thread.py
import ipaddress
import socket
from PyQt6.QtCore import QThread, pyqtSignal
import subprocess

class IPScanThread(QThread):
    output = pyqtSignal(str, str)
    finished = pyqtSignal()

    def __init__(self, ip_range):
        super().__init__()
        self.ip_range = ip_range
        self._is_running = True  # Flag to control the scanning loop

    def run(self):
        start_ip, end_ip = self.ip_range.split('-')
        try:
            start = ipaddress.IPv4Address(start_ip.strip())
            end = ipaddress.IPv4Address(end_ip.strip())
        except ValueError:
            self.finished.emit()
            return

        for ip_int in range(int(start), int(end) + 1):
            if not self._is_running:
                break  # Exit if scan is stopped

            ip = str(ipaddress.IPv4Address(ip_int))
            try:
                response = subprocess.run(
                    ["ping", "-n", "1", "-w", "100", ip],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    shell=True
                )
                if response.returncode == 0:
                    try:
                        device_name, _, _ = socket.gethostbyaddr(ip)
                    except socket.herror:
                        device_name = "Unknown"
                    # Emit only online devices
                    self.output.emit(ip, device_name)
            except Exception:
                pass
        self.finished.emit()

    def stop(self):
        self._is_running = False