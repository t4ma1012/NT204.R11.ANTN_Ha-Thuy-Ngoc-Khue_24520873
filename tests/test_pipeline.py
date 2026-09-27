from scapy.all import IP, GRE, Raw

from src.pipeline.parser_pipeline import ParserPipeline


def test_unknown_protocol_does_not_crash():
    packet = (
        IP(src="192.168.1.10", dst="192.168.1.20")
        / GRE(proto=0x88BE)
        / Raw(load=b"UNKNOWN_PROTOCOL_DATA")
    )

    pipeline = ParserPipeline()

    result = pipeline.process(packet)

    assert result is not None
    assert result["protocol"] == "unknown"

def test_malformed_packet_does_not_crash():
    pipeline = ParserPipeline()

    malformed_packet = Raw(load=b"\x45\x00\x00")

    result = pipeline.process(malformed_packet)

    assert result is not None
    assert result["protocol"] == "unknown"