from scapy.packet import Raw


def parse_smtp(packet):
    """
    Parse an SMTP command from a packet.

    Returns a dictionary containing SMTP command information.
    Returns None if the packet does not contain an SMTP command.
    """

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