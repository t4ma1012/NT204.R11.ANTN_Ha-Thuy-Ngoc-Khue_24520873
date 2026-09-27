from scapy.packet import Raw


def parse_http(packet):
    """
    Parse an HTTP request or response from a packet.

    Returns a dictionary containing HTTP information.
    Returns None if the packet is not HTTP.
    """

    if not packet.haslayer(Raw):
        return None

    payload = bytes(packet[Raw].load)
    text = payload.decode("utf-8", errors="replace")

    parts = text.split("\r\n\r\n", 1)

    header_text = parts[0]
    body = parts[1] if len(parts) > 1 else ""

    lines = header_text.split("\r\n")

    if not lines:
        return None

    first_line = lines[0]

    # HTTP response
    if first_line.startswith("HTTP/"):
        response_parts = first_line.split(" ", 2)

        if len(response_parts) < 2:
            return None

        version = response_parts[0]

        try:
            status_code = int(response_parts[1])
        except ValueError:
            return None

        reason = response_parts[2] if len(response_parts) == 3 else ""

        headers = {}

        for line in lines[1:]:
            if ":" in line:
                key, value = line.split(":", 1)
                headers[key.strip()] = value.strip()

        return {
            "type": "response",
            "version": version,
            "status_code": status_code,
            "reason": reason,
            "headers": headers,
            "body": body,
        }

    # HTTP request
    request_parts = first_line.split(" ")

    if len(request_parts) != 3:
        return None

    method, path, version = request_parts

    if method not in (
        "GET",
        "POST",
        "PUT",
        "DELETE",
        "HEAD",
        "OPTIONS",
    ):
        return None

    if not version.startswith("HTTP/"):
        return None

    headers = {}

    for line in lines[1:]:
        if ":" in line:
            key, value = line.split(":", 1)
            headers[key.strip()] = value.strip()

    return {
        "type": "request",
        "method": method,
        "path": path,
        "version": version,
        "headers": headers,
        "body": body,
    }