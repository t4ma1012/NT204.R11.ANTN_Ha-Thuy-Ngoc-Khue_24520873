from scapy.layers.inet import TCP
from scapy.packet import Raw


def parse_tcp(packet):
    """
    Parse TCP information from a Scapy packet.

    Returns a dictionary containing TCP fields and payload information.
    Returns None if the packet does not contain TCP.
    """
    if not packet.haslayer(TCP):
        return None

    tcp = packet[TCP]

    payload = b""
    if tcp.haslayer(Raw):
        payload = bytes(tcp[Raw].load)

    return {
        "src_port": tcp.sport,
        "dst_port": tcp.dport,
        "flags": str(tcp.flags),
        "seq": tcp.seq,
        "ack": tcp.ack,
        "payload_length": len(payload),
        "payload": payload.decode("utf-8", errors="replace"),
    }