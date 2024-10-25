# threads/topology_mapper_thread.py

from PyQt6.QtCore import QThread, pyqtSignal
import nmap

class TopologyMapperThread(QThread):
    output = pyqtSignal(str)
    finished = pyqtSignal(dict)  # Pass the graph data

    def __init__(self, network_range):
        super().__init__()
        self.network_range = network_range
        self._is_running = True

    def run(self):
        try:
            nm = nmap.PortScanner()
            self.output.emit(f"Scanning network: {self.network_range}")
            nm.scan(hosts=self.network_range, arguments='-sn')

            hosts = nm.all_hosts()
            self.output.emit(f"Discovered {len(hosts)} hosts.")

            nodes = []
            edges = []

            for host in hosts:
                if not self._is_running:
                    break
                hostname = nm[host].hostname()
                nodes.append((host, {'label': hostname if hostname else host}))
                # Edges can be added here if relationships are known

            # Send the data back to the main thread
            graph_data = {'nodes': nodes, 'edges': edges}
            self.output.emit("Network data collected.")
            self.finished.emit(graph_data)
        except Exception as e:
            self.output.emit(f"Error: {e}")
            self.finished.emit(None)
        finally:
            if not self._is_running:
                self.finished.emit(None)

    def stop(self):
        self._is_running = False
