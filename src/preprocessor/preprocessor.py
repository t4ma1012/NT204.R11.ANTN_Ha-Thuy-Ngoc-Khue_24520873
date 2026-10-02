from datetime import datetime, timezone
import ipaddress


class Preprocessor:
    def normalize_protocol(self, protocol):
        if not isinstance(protocol, str):
            return protocol

        return protocol.strip().upper()

    def normalize_ip(self, value):
        if not isinstance(value, str):
            return value

        value = value.strip()

        try:
            return str(ipaddress.ip_address(value))
        except ValueError:
            return value.lower()

    def normalize_headers(self, headers):
        if not isinstance(headers, dict):
            return {}

        result = {}

        for key, value in headers.items():
            normalized_key = str(key).strip().lower()

            if isinstance(value, str):
                normalized_value = value.strip()
            else:
                normalized_value = value

            result[normalized_key] = normalized_value

        return result

    def normalize_path(self, path):
        if not isinstance(path, str):
            return path

        return path.strip()

    def normalize_timestamp(self, timestamp):
        if isinstance(timestamp, (int, float)):
            return datetime.fromtimestamp(
                timestamp,
                tz=timezone.utc,
            ).isoformat()

        if isinstance(timestamp, str):
            value = timestamp.strip()

            try:
                parsed = datetime.fromisoformat(
                    value.replace("Z", "+00:00")
                )

                if parsed.tzinfo is None:
                    parsed = parsed.replace(tzinfo=timezone.utc)

                return parsed.astimezone(timezone.utc).isoformat()

            except ValueError:
                return timestamp

        return timestamp

    def process(self, event):
        result = dict(event)

        result["protocol"] = self.normalize_protocol(
            result.get("protocol")
        )

        if "src_ip" in result:
            result["src_ip"] = self.normalize_ip(
                result["src_ip"]
            )

        if "dst_ip" in result:
            result["dst_ip"] = self.normalize_ip(
                result["dst_ip"]
            )

        application = result.get("application")

        if isinstance(application, dict):
            application = dict(application)

            if "path" in application:
                application["path"] = self.normalize_path(
                    application["path"]
                )

            if "headers" in application:
                application["headers"] = self.normalize_headers(
                    application["headers"]
                )

            result["application"] = application

        if "timestamp" in result:
            result["timestamp"] = self.normalize_timestamp(
                result["timestamp"]
            )

        result["preprocess_status"] = "valid"
        result["processing_action"] = "normalized"

        return result