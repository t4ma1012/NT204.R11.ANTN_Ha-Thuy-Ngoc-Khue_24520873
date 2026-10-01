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