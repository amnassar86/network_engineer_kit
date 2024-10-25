# threads/traceroute_thread.py
from PyQt6.QtCore import QThread, pyqtSignal
import subprocess

class TracerouteThread(QThread):
    output = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, target):
        super().__init__()
        self.target = target

    def run(self):
        try:
            process = subprocess.Popen(
                ["tracert", self.target], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, shell=True
            )
            for line in iter(process.stdout.readline, ''):
                if line:
                    self.output.emit(line.strip())
            process.stdout.close()
            process.wait()
        except Exception as e:
            self.output.emit(str(e))
        finally:
            self.finished.emit()