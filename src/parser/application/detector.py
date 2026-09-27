from scapy.packet import Raw


def detect_application_protocol(packet):
    """
    Detect application protocol based on packet payload.
    """

    if not packet.haslayer(Raw):
        return None

    payload = bytes(packet[Raw].load)

    text = payload.decode("utf-8", errors="replace")

    first_line = text.split("\r\n", 1)[0]

    if first_line.startswith("HTTP/"):
        return "HTTP"

    if first_line.startswith(
        ("GET ", "POST ", "PUT ", "DELETE ", "HEAD ", "OPTIONS ")
    ):
        return "HTTP"

    return None