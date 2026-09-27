import re
from scapy.packet import Raw


def parse_smtp(packet):
    if not packet.haslayer(Raw):
        return None

    payload = bytes(packet[Raw].load)
    text = payload.decode("utf-8", errors="replace").strip()

    if not text:
        return None

    lines = text.splitlines()

    for line in lines:
        line = line.strip()
        upper_line = line.upper()

        # SMTP response: 3-digit status code
        if re.match(r"^\d{3}(?:[ -]|$)", line):
            status_code = int(line[:3])
            message = line[3:].strip()

            return {
                "type": "response",
                "status_code": status_code,
                "message": message,
            }

        # SMTP commands
        if upper_line.startswith("EHLO "):
            return {
                "type": "command",
                "command": "EHLO",
                "argument": line[5:].strip(),
            }

        if upper_line.startswith("HELO "):
            return {
                "type": "command",
                "command": "HELO",
                "argument": line[5:].strip(),
            }

        if upper_line.startswith("MAIL FROM:"):
            return {
                "type": "command",
                "command": "MAIL FROM",
                "argument": line[10:].strip(),
            }

        if upper_line.startswith("RCPT TO:"):
            return {
                "type": "command",
                "command": "RCPT TO",
                "argument": line[8:].strip(),
            }

    return None