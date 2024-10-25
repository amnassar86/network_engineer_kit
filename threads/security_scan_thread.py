# threads/security_scan_thread.py

from PyQt6.QtCore import QThread, pyqtSignal
import nmap

class SecurityScanThread(QThread):
    output = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, target):
        super().__init__()
        self.target = target
        self._is_running = True

    def run(self):
        try:
            nm = nmap.PortScanner()
            self.output.emit(f"Starting security scan on {self.target}")
            nm.scan(self.target, arguments='-sV -O')

            for host in nm.all_hosts():
                if not self._is_running:
                    break
                self.output.emit(f"Host: {host} ({nm[host].hostname()})")
                self.output.emit(f"State: {nm[host].state()}")

                # Services and versions
                for proto in nm[host].all_protocols():
                    lport = nm[host][proto].keys()
                    for port in lport:
                        service = nm[host][proto][port]
                        self.output.emit(f"Port: {port}/{proto}")
                        self.output.emit(f"Service: {service['name']}")
                        self.output.emit(f"Version: {service['version']}")
                        self.output.emit(f"Product: {service['product']}")
                        self.output.emit("-" * 20)

                # OS Detection
                if 'osmatch' in nm[host]:
                    for osmatch in nm[host]['osmatch']:
                        self.output.emit(f"OS: {osmatch['name']} ({osmatch['accuracy']}% accuracy)")
                        break  # Take the first match
                self.output.emit("=" * 40)
            self.finished.emit()
        except Exception as e:
            self.output.emit(f"Error: {e}")
            self.finished.emit()
        finally:
            if not self._is_running:
                self.finished.emit()

    def stop(self):
        self._is_running = False
