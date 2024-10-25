# threads/packet_sniffer_thread.py

from PyQt6.QtCore import QThread, pyqtSignal
import scapy.all as scapy

class PacketSnifferThread(QThread):
    output = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, iface, bpf_filter, promiscuous):
        super().__init__()
        self.iface = iface
        self.bpf_filter = bpf_filter
        self.promiscuous = promiscuous
        self._is_running = True

    def run(self):
        try:
            scapy.sniff(
                iface=self.iface,
                prn=self.process_packet,
                filter=self.bpf_filter,
                store=False,
                promisc=self.promiscuous,
                stop_filter=lambda x: not self._is_running
            )
        except Exception as e:
            self.output.emit(f"Error: {e}")
        finally:
            self.finished.emit()

    def process_packet(self, packet):
        if not self._is_running:
            return False
        summary = packet.summary()
        self.output.emit(summary)

    def stop(self):
        self._is_running = False
