from .port_info import PortInfo
from typing import List, Dict

class CollectorInfo(object):
    """
    Define structure of the information of a collector host that
    will be exchanged via probe_init packet
    """
    def __init__(self, inet_addr: str, ports: List[PortInfo]):
        self.inet_addr = inet_addr
        self.ports = ports

    def __str__(self):
        return "{}:{}".format(self.inet_addr, str(self.ports))

    def __repr__(self):
        return "{}({}:{})".format(self.__class__.__name__, self.inet_addr, self.ports)

    def daemon_fqinfo(self) -> List[Dict]:
        daemons = []
        for info in self.ports:
            daemons.append({'daemon': info.daemon,
                            'fqinfo': (self.inet_addr, info.port)})

        return daemons