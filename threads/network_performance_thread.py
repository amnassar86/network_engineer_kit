# threads/network_performance_thread.py

from PyQt6.QtCore import QThread, pyqtSignal
import iperf3

class NetworkPerformanceThread(QThread):
    output = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, server_ip):
        super().__init__()
        self.server_ip = server_ip
        self._is_running = True

    def run(self):
        try:
            client = iperf3.Client()
            client.server_hostname = self.server_ip
            client.port = 5201
            self.output.emit(f"Connecting to {self.server_ip} on port 5201...")
            result = client.run()
            if result.error:
                self.output.emit(f"Error: {result.error}")
            else:
                self.output.emit(f"Test Completed:\n"
                                 f"Download: {result.received_Mbps:.2f} Mbps\n"
                                 f"Upload: {result.sent_Mbps:.2f} Mbps\n"
                                 f"Latency: {result.ping_avg} ms")
        except Exception as e:
            self.output.emit(f"Exception: {e}")
        finally:
            self.finished.emit()

    def stop(self):
        self._is_running = False
