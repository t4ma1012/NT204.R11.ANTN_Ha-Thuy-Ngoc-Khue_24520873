from src.parser.transport.tcp import parse_tcp


class ParserPipeline:
    """
    Common parsing pipeline for packets coming from
    live capture or PCAP input.
    """

    def process(self, packet):
        """
        Process one raw packet through the parsing pipeline.

        For the current task, TCP packets are parsed.
        """

        tcp_data = parse_tcp(packet)

        if tcp_data is None:
            return {
                "protocol": "unknown"
            }

        return {
            "protocol": "TCP",
            "transport": tcp_data
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