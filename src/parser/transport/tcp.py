from scapy.layers.inet import TCP


def parse_tcp(packet):
    """
    Parse TCP information from a Scapy packet.

    Returns a dictionary containing TCP fields.
    Returns None if the packet does not contain TCP.
    """

    if not packet.haslayer(TCP):
        return None

    tcp = packet[TCP]

    return {
        "src_port": tcp.sport,
        "dst_port": tcp.dport,
        "flags": str(tcp.flags),
        "seq": tcp.seq,
        "ack": tcp.ack,
    }