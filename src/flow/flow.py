class Flow:
    def __init__(
        self,
        flow_id,
        protocol,
        endpoint_a,
        endpoint_b,
        start_time,
    ):
        self.flow_id = flow_id
        self.protocol = protocol

        self.endpoint_a = endpoint_a
        self.endpoint_b = endpoint_b

        self.start_time = start_time
        self.last_seen = start_time

        self.packet_count = 0
        self.byte_count = 0

        self.forward_packets = 0
        self.backward_packets = 0

        self.forward_bytes = 0
        self.backward_bytes = 0

        self.syn_count = 0
        self.ack_count = 0
        self.fin_count = 0
        self.rst_count = 0

        self.tcp_state = (
            "NEW" if protocol == "TCP" else None
        )

    def duration(self):
        return self.last_seen - self.start_time

    def to_dict(self):
        return {
            "flow_id": self.flow_id,
            "protocol": self.protocol,
            "endpoints": [
                self.endpoint_a,
                self.endpoint_b,
            ],
            "start_time": self.start_time,
            "last_seen": self.last_seen,
            "duration": self.duration(),
            "packet_count": self.packet_count,
            "byte_count": self.byte_count,
            "forward_packets": self.forward_packets,
            "backward_packets": self.backward_packets,
            "forward_bytes": self.forward_bytes,
            "backward_bytes": self.backward_bytes,
            "syn_count": self.syn_count,
            "ack_count": self.ack_count,
            "fin_count": self.fin_count,
            "rst_count": self.rst_count,
            "tcp_state": self.tcp_state,
        }