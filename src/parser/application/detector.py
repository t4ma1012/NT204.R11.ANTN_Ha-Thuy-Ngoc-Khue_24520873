import re

from scapy.packet import Raw
from scapy.layers.dns import DNS


def detect_application_protocol(packet):
    if packet.haslayer(DNS):
        return "DNS"

    if not packet.haslayer(Raw):
        return None

    payload = bytes(packet[Raw].load)
    text = payload.decode("utf-8", errors="replace")
    lines = text.splitlines()

    if not lines:
        return None

    first_line = lines[0].strip()

    # HTTP response
    if first_line.startswith("HTTP/"):
        return "HTTP"

    # HTTP request
    if first_line.startswith(
        ("GET ", "POST ", "PUT ", "DELETE ", "HEAD ", "OPTIONS ")
    ):
        return "HTTP"

    upper_line = first_line.upper()

    # SMTP commands
    if (
        upper_line.startswith("EHLO ")
        or upper_line.startswith("HELO ")
        or upper_line.startswith("MAIL FROM:")
        or upper_line.startswith("RCPT TO:")
    ):
        return "SMTP"

    # SMTP response
    if re.match(r"^\d{3}(?:[ -]|$)", first_line):
        return "SMTP"

    return None