from src.decoder.decoder import Decoder

# test 01
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

    assert application["raw_path"] == "/search?q=%27%20OR%201%3D1"

    assert application["decoded_path"] == "/search?q=' OR 1=1"

# test 02

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


# Test T03
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

    assert base64_application["raw_body"] == "SGVsbG8gV29ybGQh"
    assert base64_application["decoded_body"] == "Hello World!"
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

    assert qp_application["raw_body"] == "Hello=20World=21"
    assert qp_application["decoded_body"] == "Hello World!"
    assert qp_application["decode_status"] == "success"