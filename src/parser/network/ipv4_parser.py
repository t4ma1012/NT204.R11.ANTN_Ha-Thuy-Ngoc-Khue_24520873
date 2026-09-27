from scapy.layers.inet import IP


def parse_ipv4(packet):
    """
    Parse IPv4 information from a Scapy packet.

    Returns:
        dict: Normalized IPv4 information.
        None: If the packet does not contain IPv4.
    """

    if not packet.haslayer(IP):
        return None

    ip = packet[IP]

    return {
        "src_ip": ip.src,
        "dst_ip": ip.dst,
        "protocol": ip.proto,
        "ttl": ip.ttl,
        "packet_length": ip.len,
    }