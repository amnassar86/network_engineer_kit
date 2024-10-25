# threads/ping_thread.py
from PyQt6.QtCore import QThread, pyqtSignal
import subprocess

class ARPThread(QThread):
    output = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, target_ip):
        super().__init__()
        self.target_ip = target_ip

    def run(self):
        try:
            result = subprocess.Popen(
                ["arp", "-a", self.target_ip],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                shell=True
            )
            for line in iter(result.stdout.readline, ''):
                if line:
                    self.output.emit(line.strip())
            result.stdout.close()
            result.wait()
        except Exception as e:
            self.output.emit(str(e))
        finally:
            self.finished.emit()