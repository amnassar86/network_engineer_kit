# threads/wifi_scan_thread.py

from PyQt6.QtCore import QThread, pyqtSignal
import subprocess
import platform
import re

class WifiScanThread(QThread):
    output = pyqtSignal(str, str, str, str)
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()

    def run(self):
        system = platform.system().lower()
        if system == 'windows':
            cmd = ["netsh", "wlan", "show", "networks", "mode=Bssid"]
            ssid_pattern = re.compile(r"SSID\s+\d+\s+:\s+(.*)")
            bssid_pattern = re.compile(r"BSSID\s+\d+\s+:\s+(.*)")
            signal_pattern = re.compile(r"Signal\s+:\s+(.*)%")
            channel_pattern = re.compile(r"Channel\s+:\s+(.*)")
            try:
                output = subprocess.check_output(cmd, text=True)
                ssids = ssid_pattern.findall(output)
                bssids = bssid_pattern.findall(output)
                signals = signal_pattern.findall(output)
                channels = channel_pattern.findall(output)
                for i in range(len(ssids)):
                    self.output.emit(ssids[i], bssids[i], signals[i] + "%", channels[i])
            except Exception as e:
                pass
        elif system == 'linux':
            cmd = ["sudo", "iwlist", "scan"]
            cell_pattern = re.compile(r"Cell \d+ - Address: (.*)")
            ssid_pattern = re.compile(r"ESSID:\"(.*)\"")
            signal_pattern = re.compile(r"Signal level=(.*) dBm")
            channel_pattern = re.compile(r"Channel:(\d+)")
            try:
                output = subprocess.check_output(cmd, text=True)
                cells = cell_pattern.findall(output)
                ssids = ssid_pattern.findall(output)
                signals = signal_pattern.findall(output)
                channels = channel_pattern.findall(output)
                for i in range(len(cells)):
                    self.output.emit(ssids[i], cells[i], signals[i] + " dBm", channels[i])
            except Exception as e:
                pass
        else:
            # Not supported on this platform
            pass

        self.finished.emit()
