from .metric_info import MetricInfo
from .vrm_type import VrmType

class MetricInit(object):
    """
    System packet that will be encapsulated inside an UDP packet
    and sent back to collector host by worker
    """
    def __init__(self, packet_id: str, info: 'MetricInfo', packet_type: 'VrmType'):
        self.packet_id = packet_id
        self.info = info
        self.type = packet_type

    def __str__(self):
        return "[{}] {} - {}".format(str(self.type), id, str(self.info))

    def __repr__(self):
        return "{}({} - {})".format(self.__class__.__name__,
                                    id,
                                    str(self.info))