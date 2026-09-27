from scapy.all import IP, UDP, DNS, DNSQR

from src.parser.application.dns import parse_dns


def test_dns_query():
    packet = (
        IP(src="192.168.1.10", dst="8.8.8.8")
        / UDP(sport=12345, dport=53)
        / DNS(
            id=0x1234,
            qr=0,
            rd=1,
            qd=DNSQR(
                qname="example.com",
                qtype="A"
            )
        )
    )

    result = parse_dns(packet)

    assert result is not None
    assert result["type"] == "query"
    assert result["query"]["name"] == "example.com."
    assert result["query"]["type"] == 1
    assert result["query"]["class"] == 1