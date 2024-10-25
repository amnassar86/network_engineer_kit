# threads/snmp_thread.py

from PyQt6.QtCore import QThread, pyqtSignal
from pysnmp.hlapi import *

class SNMPThread(QThread):
    output = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, ip_address, community, oid):
        super().__init__()
        self.ip_address = ip_address
        self.community = community
        self.oid = oid

    def run(self):
        try:
            iterator = getCmd(
                SnmpEngine(),
                CommunityData(self.community, mpModel=0),
                UdpTransportTarget((self.ip_address, 161)),
                ContextData(),
                ObjectType(ObjectIdentity(self.oid))
            )

            errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

            if errorIndication:
                self.output.emit(f"Error: {errorIndication}")
            elif errorStatus:
                self.output.emit(f"{errorStatus.prettyPrint()}")
            else:
                for varBind in varBinds:
                    self.output.emit(f"{varBind}")
        except Exception as e:
            self.output.emit(f"Exception: {e}")
        finally:
            self.finished.emit()
