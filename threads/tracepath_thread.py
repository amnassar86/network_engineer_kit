# threads/tracepath_thread.py

from PyQt6.QtCore import QThread, pyqtSignal
import subprocess
import platform

class TracepathThread(QThread):
    output = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, target):
        super().__init__()
        self.target = target

    def run(self):
        system = platform.system().lower()
        if system == 'linux':
            cmd = ["tracepath", self.target]
        elif system == 'windows':
            self.output.emit("Tracepath is not available on Windows.")
            self.finished.emit()
            return
        else:
            self.output.emit(f"Tracepath is not supported on {platform.system()}.")
            self.finished.emit()
            return

        try:
            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
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
