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

    # Parse DNS question
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

    # Parse DNS answer
    if dns.an is not None:
        answers = []

        for answer in dns.an:
            rrname = answer.rrname

            if isinstance(rrname, bytes):
                rrname = rrname.decode("utf-8", errors="replace")

            rdata = answer.rdata

            if isinstance(rdata, bytes):
                rdata = rdata.decode("utf-8", errors="replace")

            answers.append({
                "name": rrname,
                "type": answer.type,
                "class": answer.rclass,
                "ttl": answer.ttl,
                "data": rdata,
            })

        result["answers"] = answers

    return result