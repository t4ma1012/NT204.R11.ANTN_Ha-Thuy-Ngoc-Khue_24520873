from scapy.layers.inet import IP, TCP

from src.parser.transport.tcp import parse_tcp

def test_tcp_syn():
    packet = IP(
        src="10.0.0.1",
        dst="10.0.0.2"
    ) / TCP(
        sport=12345,
        dport=80,
        flags="S",
        seq=1000
    )

    result = parse_tcp(packet)

    assert result is not None
    assert result["src_port"] == 12345
    assert result["dst_port"] == 80
    assert result["flags"] == "S"


def test_tcp_syn_ack():
    packet = IP(
        src="10.0.0.2",
        dst="10.0.0.1"
    ) / TCP(
        sport=80,
        dport=12345,
        flags="SA",
        seq=2000,
        ack=1001
    )

    result = parse_tcp(packet)

    assert result is not None
    assert result["flags"] == "SA"


def test_tcp_ack():
    packet = IP(
        src="10.0.0.1",
        dst="10.0.0.2"
    ) / TCP(
        sport=12345,
        dport=80,
        flags="A",
        seq=1001,
        ack=2001
    )

    result = parse_tcp(packet)

    assert result is not None
    assert result["flags"] == "A"