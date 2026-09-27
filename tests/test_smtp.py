from scapy.all import IP, TCP, Raw

from src.parser.application.smtp import parse_smtp


def test_smtp_ehlo():
    packet = (
        IP(src="10.81.31.230", dst="10.82.232.33")
        / TCP(sport=48350, dport=25, flags="PA")
        / Raw(load=b"EHLO attacker\n")
    )

    result = parse_smtp(packet)

    assert result is not None
    assert result["type"] == "command"
    assert result["command"] == "EHLO"
    assert result["argument"] == "attacker"