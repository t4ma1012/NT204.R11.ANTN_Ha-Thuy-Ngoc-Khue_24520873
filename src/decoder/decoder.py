import base64
import binascii
import copy
import html
from email import quoprimime
from urllib.parse import unquote, unquote_plus


class Decoder:
    def decode_uri(self, uri):
        if not isinstance(uri, str):
            return uri

        return unquote(uri)

    def decode_form_value(self, value):
        if not isinstance(value, str):
            return value

        return unquote_plus(value)

    def decode_html(self, text):
        if not isinstance(text, str):
            return text

        return html.unescape(text)

    def decode_base64(self, value):
        if not isinstance(value, str):
            return value, "invalid"

        try:
            decoded = base64.b64decode(value, validate=True)
            text = decoded.decode("utf-8")
            return text, "success"

        except (binascii.Error, UnicodeDecodeError):
            return value, "error"

    def decode_quoted_printable(self, value):
        if not isinstance(value, str):
            return value, "invalid"

        try:
            decoded = quoprimime.body_decode(value)
            return decoded, "success"

        except Exception:
            return value, "error"

    def decode_text(self, value, encoding="utf-8"):
        if isinstance(value, str):
            return value, "success"

        if not isinstance(value, (bytes, bytearray)):
            return value, "invalid"

        try:
            return bytes(value).decode(encoding), "success"

        except UnicodeDecodeError:
            return (
                bytes(value).decode(encoding, errors="replace"),
                "partial",
            )

    def decode_event(self, event):
        result = copy.deepcopy(event)

        application = result.get("application")

        if not isinstance(application, dict):
            return result

        protocol = result.get("protocol")

        if protocol == "HTTP":
            self._decode_http(application)

        elif protocol == "SMTP":
            self._decode_smtp(application)

        return result

    def _decode_http(self, application):
        path = application.get("path")

        if isinstance(path, str):
            application["raw_path"] = path
            application["decoded_path"] = self.decode_uri(path)

        body = application.get("body")

        if isinstance(body, str):
            application["raw_body"] = body
            application["decoded_body"] = self.decode_html(body)

    def _decode_smtp(self, application):
        body = application.get("body")

        if not isinstance(body, str):
            return

        application["raw_body"] = body

        headers = application.get("headers", {})
        encoding = headers.get("Content-Transfer-Encoding")

        if not isinstance(encoding, str):
            application["decoded_body"] = body
            application["decode_status"] = "not_encoded"
            return

        encoding = encoding.lower().strip()

        if encoding == "base64":
            decoded, status = self.decode_base64(body)

        elif encoding == "quoted-printable":
            decoded, status = self.decode_quoted_printable(body)

        else:
            decoded = body
            status = "unsupported"

        application["decoded_body"] = decoded
        application["decode_status"] = status