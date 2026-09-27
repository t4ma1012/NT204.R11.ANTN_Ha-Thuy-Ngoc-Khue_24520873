from scapy.packet import Raw
from scapy.layers.dns import DNS


def detect_application_protocol(packet):
    """
    Detect application protocol based on packet structure and payload.
    """

    # DNS detection
    if packet.haslayer(DNS):
        return "DNS"

    # Payload-based detection
    if not packet.haslayer(Raw):
        return None

    payload = bytes(packet[Raw].load)

    text = payload.decode("utf-8", errors="replace")

    first_line = text.splitlines()[0].strip() if text.splitlines() else ""

    # HTTP response
    if first_line.startswith("HTTP/"):
        return "HTTP"

    # HTTP request
    if first_line.startswith(
        ("GET ", "POST ", "PUT ", "DELETE ", "HEAD ", "OPTIONS ")
    ):
        return "HTTP"

    # SMTP command
    upper_line = first_line.upper()

    if (
        upper_line.startswith("EHLO ")
        or upper_line.startswith("HELO ")
        or upper_line.startswith("MAIL FROM:")
        or upper_line.startswith("RCPT TO:")
    ):
        return "SMTP"

    return None