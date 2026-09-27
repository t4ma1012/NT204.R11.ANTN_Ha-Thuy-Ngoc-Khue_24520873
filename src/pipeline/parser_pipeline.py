from src.parser.transport.tcp import parse_tcp
from src.parser.transport.udp import parse_udp
from src.parser.application.detector import detect_application_protocol
from src.parser.application.http import parse_http
from src.parser.application.dns import parse_dns


class ParserPipeline:
    """
    Common parsing pipeline for packets coming from
    live capture or PCAP input.
    """

    def process(self, packet):
        """
        Process one packet through the parsing pipeline.
        """

        # TCP
        tcp_data = parse_tcp(packet)

        if tcp_data is not None:
            application_protocol = detect_application_protocol(packet)

            if application_protocol == "HTTP":
                http_data = parse_http(packet)

                if http_data is not None:
                    return {
                        "protocol": "HTTP",
                        "transport": tcp_data,
                        "application": http_data,
                    }

            return {
                "protocol": "TCP",
                "transport": tcp_data,
            }

        # UDP
        udp_data = parse_udp(packet)

        if udp_data is not None:
            application_protocol = detect_application_protocol(packet)

            if application_protocol == "DNS":
                dns_data = parse_dns(packet)

                if dns_data is not None:
                    return {
                        "protocol": "DNS",
                        "transport": udp_data,
                        "application": dns_data,
                    }

            return {
                "protocol": "UDP",
                "transport": udp_data,
            }

        # Unknown protocol
        return {
            "protocol": "unknown"
        }

    def process_packets(self, packets):
        results = []

        for packet in packets:
            result = self.process(packet)
            results.append(result)

        return results