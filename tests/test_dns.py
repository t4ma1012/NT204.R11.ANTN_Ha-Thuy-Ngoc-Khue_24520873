from scapy.all import IP, UDP, DNS, DNSQR, DNSRR

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


def test_dns_response():
    packet = (
        IP(src="8.8.8.8", dst="192.168.1.10")
        / UDP(sport=53, dport=12345)
        / DNS(
            id=0x1234,
            qr=1,
            aa=1,
            qd=DNSQR(
                qname="example.com",
                qtype="A"
            ),
            an=DNSRR(
                rrname="example.com",
                type="A",
                rdata="93.184.216.34",
                ttl=300
            )
        )
    )

    result = parse_dns(packet)

    assert result is not None
    assert result["type"] == "response"
    assert result["query"]["name"] == "example.com."
    assert result["query"]["type"] == 1

    assert len(result["answers"]) >= 1
    assert result["answers"][0]["name"] == "example.com."
    assert result["answers"][0]["type"] == 1
    assert result["answers"][0]["data"] == "93.184.216.34"
    assert result["answers"][0]["ttl"] == 300