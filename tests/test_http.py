from scapy.all import IP, TCP, Raw

from src.parser.application.detector import detect_application_protocol
from src.parser.application.http import parse_http


def test_http_get():
    payload = (
        b"GET /index.html HTTP/1.1\r\n"
        b"Host: example.com\r\n"
        b"User-Agent: test-client\r\n"
        b"Accept: */*\r\n"
        b"\r\n"
    )

    packet = (
        IP(src="192.168.1.10", dst="192.168.1.20")
        / TCP(sport=12345, dport=80, flags="PA")
        / Raw(load=payload)
    )

    assert detect_application_protocol(packet) == "HTTP"

    result = parse_http(packet)

    assert result is not None
    assert result["method"] == "GET"
    assert result["path"] == "/index.html"
    assert result["version"] == "HTTP/1.1"
    assert result["headers"]["Host"] == "example.com"
    assert result["headers"]["User-Agent"] == "test-client"
    assert result["headers"]["Accept"] == "*/*"