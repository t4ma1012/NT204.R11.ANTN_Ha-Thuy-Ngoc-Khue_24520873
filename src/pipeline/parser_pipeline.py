from src.parser.transport.tcp import parse_tcp
from src.parser.transport.udp import parse_udp


class ParserPipeline:
    """
    Common parsing pipeline for packets coming from
    live capture or PCAP input.
    """

    def process(self, packet):
        """
        Process one packet through the transport parsers.
        """

        tcp_data = parse_tcp(packet)

        if tcp_data is not None:
            return {
                "protocol": "TCP",
                "transport": tcp_data
            }

        udp_data = parse_udp(packet)

        if udp_data is not None:
            return {
                "protocol": "UDP",
                "transport": udp_data
            }

        return {
            "protocol": "unknown"
        }

    def process_packets(self, packets):
        """
        Process a collection of packets using the same pipeline.
        """
        results = []

        for packet in packets:
            result = self.process(packet)
            results.append(result)

        return results