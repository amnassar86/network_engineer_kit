# threads/bandwidth_monitor_thread.py
from PyQt6.QtCore import QThread, pyqtSignal
import subprocess
import time
import random

class BandwidthMonitorThread(QThread):
    output = pyqtSignal(str)
    finished = pyqtSignal(float, float)  # Emit average download and upload speeds

    def __init__(self):
        super().__init__()
        self.download_speeds = []
        self.upload_speeds = []

    def run(self):
        start_time = time.time()
        while time.time() - start_time < 10:  # Adjusted for quicker testing
            # Simulate bandwidth data
            download_speed = random.uniform(10, 100)  # In Mbps
            upload_speed = random.uniform(5, 50)      # In Mbps
            timestamp = time.strftime("%H:%M:%S", time.localtime())

            # Store the speeds
            self.download_speeds.append(download_speed)
            self.upload_speeds.append(upload_speed)

            self.output.emit(f"{timestamp} - Download: {download_speed:.2f} Mbps, Upload: {upload_speed:.2f} Mbps")
            time.sleep(1)

        # Calculate average speeds
        avg_download = sum(self.download_speeds) / len(self.download_speeds)
        avg_upload = sum(self.upload_speeds) / len(self.upload_speeds)

        # Emit the averages
        self.finished.emit(avg_download, avg_upload)