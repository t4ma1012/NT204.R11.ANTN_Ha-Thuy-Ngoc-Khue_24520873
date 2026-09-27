from scapy.all import IP

from src.parser.network.ipv4_parser import parse_ipv4


def test_ipv4_parser():
    packet = IP(
        src="192.168.1.10",
        dst="192.168.1.20",
        ttl=64
    )

    result = parse_ipv4(packet)

    assert result is not None
    assert result["src_ip"] == "192.168.1.10"
    assert result["dst_ip"] == "192.168.1.20"
    assert result["ttl"] == 64