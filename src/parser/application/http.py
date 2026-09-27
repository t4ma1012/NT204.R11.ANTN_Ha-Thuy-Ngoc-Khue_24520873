from scapy.packet import Raw


def parse_http(packet):
    """
    Parse a HTTP request from a packet.

    Returns a dictionary containing HTTP method,
    path, version, and headers.
    Returns None if the packet is not HTTP.
    """

    if not packet.haslayer(Raw):
        return None

    payload = bytes(packet[Raw].load)

    try:
        text = payload.decode("utf-8", errors="replace")
    except Exception:
        return None

    lines = text.split("\r\n")

    if not lines:
        return None

    request_line = lines[0]

    parts = request_line.split(" ")

    if len(parts) != 3:
        return None

    method, path, version = parts

    if method not in ("GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"):
        return None

    if not version.startswith("HTTP/"):
        return None

    headers = {}

    for line in lines[1:]:
        if not line:
            break

        if ":" in line:
            key, value = line.split(":", 1)
            headers[key.strip()] = value.strip()

    return {
        "method": method,
        "path": path,
        "version": version,
        "headers": headers,
    }