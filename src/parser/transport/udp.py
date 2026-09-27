from scapy.layers.inet import UDP
from scapy.packet import Raw


def parse_udp(packet):
    """
    Parse UDP information from a Scapy packet.

    Returns a dictionary containing UDP fields and payload information.
    Returns None if the packet does not contain UDP.
    """
    if not packet.haslayer(UDP):
        return None

    udp = packet[UDP]

    payload = b""
    if udp.haslayer(Raw):
        payload = bytes(udp[Raw].load)

    return {
        "src_port": udp.sport,
        "dst_port": udp.dport,
        "length": udp.len,
        "payload_length": len(payload),
        "payload": payload.decode("utf-8", errors="replace"),
    }