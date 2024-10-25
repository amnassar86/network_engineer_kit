# threads/dns_lookup_thread.py

from PyQt6.QtCore import QThread, pyqtSignal
import dns.resolver

class DNSLookupThread(QThread):
    output = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, domain, record_type):
        super().__init__()
        self.domain = domain
        self.record_type = record_type

    def run(self):
        try:
            answers = dns.resolver.resolve(self.domain, self.record_type)
            for rdata in answers:
                self.output.emit(str(rdata))
        except Exception as e:
            self.output.emit(f"Error: {e}")
        finally:
            self.finished.emit()
