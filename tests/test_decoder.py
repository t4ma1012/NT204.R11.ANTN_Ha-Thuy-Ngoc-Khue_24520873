import json
from pathlib import Path

from src.decoder.decoder import Decoder

# T01
def write_output(path, data):
    output_file = Path(path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    output_file.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
#T02

def test_http_url_percent_decode():
    decoder = Decoder()

    event = {
        "protocol": "HTTP",
        "application": {
            "type": "request",
            "method": "GET",
            "path": "/search?q=%27%20OR%201%3D1",
            "version": "HTTP/1.1",
            "headers": {},
            "body": "",
        },
    }

    result = decoder.decode_event(event)
    application = result["application"]

    assert application["raw_path"] == (
        "/search?q=%27%20OR%201%3D1"
    )

    assert application["decoded_path"] == (
        "/search?q=' OR 1=1"
    )

    write_output(
        "TEST/decoder/http_url/output.json",
        result,
    )

# T03
def test_html_entity_decode():
    decoder = Decoder()

    event = {
        "protocol": "HTTP",
        "application": {
            "type": "request",
            "method": "POST",
            "path": "/comment",
            "version": "HTTP/1.1",
            "headers": {},
            "body": "&lt;script&gt;alert(&quot;x&quot;)&lt;/script&gt;",
        },
    }

    result = decoder.decode_event(event)
    application = result["application"]

    assert application["raw_body"] == (
        "&lt;script&gt;alert(&quot;x&quot;)&lt;/script&gt;"
    )

    assert application["decoded_body"] == (
        '<script>alert("x")</script>'
    )

    write_output(
        "TEST/decoder/html_entity/output.json",
        result,
    )

#T04
def test_smtp_mime_base64_and_quoted_printable():
    decoder = Decoder()

    # Base64
    base64_event = {
        "protocol": "SMTP",
        "application": {
            "type": "data",
            "headers": {
                "Content-Transfer-Encoding": "base64"
            },
            "body": "SGVsbG8gV29ybGQh",
        },
    }

    base64_result = decoder.decode_event(base64_event)
    base64_application = base64_result["application"]

    assert base64_application["raw_body"] == (
        "SGVsbG8gV29ybGQh"
    )

    assert base64_application["decoded_body"] == (
        "Hello World!"
    )

    assert base64_application["decode_status"] == "success"

    # Quoted-Printable
    qp_event = {
        "protocol": "SMTP",
        "application": {
            "type": "data",
            "headers": {
                "Content-Transfer-Encoding": "quoted-printable"
            },
            "body": "Hello=20World=21",
        },
    }

    qp_result = decoder.decode_event(qp_event)
    qp_application = qp_result["application"]

    assert qp_application["raw_body"] == (
        "Hello=20World=21"
    )

    assert qp_application["decoded_body"] == (
        "Hello World!"
    )

    assert qp_application["decode_status"] == "success"

    output = {
        "base64": base64_result,
        "quoted_printable": qp_result,
    }

    write_output(
        "TEST/decoder/smtp_mime/output.json",
        output,
    )

# T05
def test_invalid_utf8_bytes():
    decoder = Decoder()

    invalid_bytes = b"Hello \xff World"

    decoded, status = decoder.decode_text(invalid_bytes)

    assert status == "partial"
    assert "\ufffd" in decoded

    output = {
        "input": {
            "type": "bytes",
            "value": list(invalid_bytes),
        },
        "output": {
            "decoded": decoded,
            "decode_status": status,
        },
    }

    write_output(
        "TEST/decoder/invalid_bytes/output.json",
        output,
    )