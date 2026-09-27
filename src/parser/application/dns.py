from scapy.layers.dns import DNS


def parse_dns(packet):
    """
    Parse a DNS query or response from a Scapy packet.

    Returns a dictionary containing DNS information.
    Returns None if the packet does not contain DNS.
    """

    if not packet.haslayer(DNS):
        return None

    dns = packet[DNS]

    result = {
        "type": "query" if dns.qr == 0 else "response",
    }

    if dns.qd is not None:
        question = dns.qd

        qname = question.qname
        if isinstance(qname, bytes):
            qname = qname.decode("utf-8", errors="replace")

        result["query"] = {
            "name": qname,
            "type": question.qtype,
            "class": question.qclass,
        }

    return result