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


def test_http_post():
    payload = (
        b"POST /ping.php HTTP/1.1\r\n"
        b"Host: example.com\r\n"
        b"Content-Length: 11\r\n"
        b"Content-Type: application/x-www-form-urlencoded\r\n"
        b"\r\n"
        b"hello=world"
    )

    packet = (
        IP(src="192.168.1.10", dst="192.168.1.20")
        / TCP(sport=12345, dport=80, flags="PA")
        / Raw(load=payload)
    )

    assert detect_application_protocol(packet) == "HTTP"

    result = parse_http(packet)

    assert result is not None
    assert result["method"] == "POST"
    assert result["path"] == "/ping.php"
    assert result["version"] == "HTTP/1.1"
    assert result["headers"]["Host"] == "example.com"
    assert result["headers"]["Content-Length"] == "11"
    assert result["headers"]["Content-Type"] == "application/x-www-form-urlencoded"
    assert result["body"] == "hello=world"

def test_http_response():
    payload = (
        b"HTTP/1.1 200 OK\r\n"
        b"Server: Apache\r\n"
        b"Content-Length: 5\r\n"
        b"Content-Type: text/html\r\n"
        b"\r\n"
        b"Hello"
    )

    packet = (
        IP(src="192.168.1.20", dst="192.168.1.10")
        / TCP(sport=80, dport=12345, flags="PA")
        / Raw(load=payload)
    )

    assert detect_application_protocol(packet) == "HTTP"

    result = parse_http(packet)

    assert result is not None
    assert result["type"] == "response"
    assert result["version"] == "HTTP/1.1"
    assert result["status_code"] == 200
    assert result["reason"] == "OK"
    assert result["headers"]["Server"] == "Apache"
    assert result["headers"]["Content-Length"] == "5"
    assert result["headers"]["Content-Type"] == "text/html"
    assert result["body"] == "Hello"