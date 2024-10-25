# threads/latency_jitter_thread.py

from PyQt6.QtCore import QThread, pyqtSignal
import time
import subprocess
import platform

class LatencyJitterThread(QThread):
    output = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, target):
        super().__init__()
        self.target = target
        self._is_running = True

    def run(self):
        latencies = []
        previous_latency = None

        while self._is_running:
            try:
                if platform.system().lower() == "windows":
                    cmd = ["ping", self.target, "-n", "1", "-w", "1000"]
                else:
                    cmd = ["ping", "-c", "1", "-W", "1", self.target]

                start_time = time.time()
                response = subprocess.run(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                end_time = time.time()
                elapsed_time = (end_time - start_time) * 1000  # Convert to milliseconds

                if response.returncode == 0:
                    latencies.append(elapsed_time)
                    if len(latencies) > 1:
                        jitter = abs(latencies[-1] - latencies[-2])
                    else:
                        jitter = 0.0
                    self.output.emit(f"Latency: {elapsed_time:.2f} ms, Jitter: {jitter:.2f} ms")
                else:
                    self.output.emit("Request timed out.")
                time.sleep(1)
            except Exception as e:
                self.output.emit(f"Error: {e}")
                break

        self.finished.emit()

    def stop(self):
        self._is_running = False
