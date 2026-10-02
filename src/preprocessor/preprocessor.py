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
                    parsed = parsed.replace(
                        tzinfo=timezone.utc
                    )

                return parsed.astimezone(
                    timezone.utc
                ).isoformat()

            except ValueError:
                return timestamp

        return timestamp

    def process(self, event):
        # Event không phải dictionary
        if not isinstance(event, dict):
            return {
                "preprocess_status": "invalid",
                "processing_action": "drop",
                "reason": "event must be a dictionary",
            }

        # Copy event để không sửa dữ liệu đầu vào
        result = dict(event)

        # -------------------------
        # Normalize protocol
        # -------------------------

        result["protocol"] = self.normalize_protocol(
            result.get("protocol")
        )

        # -------------------------
        # Normalize IP
        # -------------------------

        if "src_ip" in result:
            result["src_ip"] = self.normalize_ip(
                result["src_ip"]
            )
        else:
            result["src_ip"] = None

        if "dst_ip" in result:
            result["dst_ip"] = self.normalize_ip(
                result["dst_ip"]
            )
        else:
            result["dst_ip"] = None

        # -------------------------
        # Normalize application
        # -------------------------

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
            else:
                application["headers"] = {}

            result["application"] = application

        elif application is None:
            result["application"] = {}

        # -------------------------
        # Normalize timestamp
        # -------------------------

        if "timestamp" in result:
            result["timestamp"] = self.normalize_timestamp(
                result["timestamp"]
            )
        else:
            result["timestamp"] = None

        # -------------------------
        # Validate required fields
        # -------------------------

        missing_fields = []

        required_fields = [
            "timestamp",
            "protocol",
            "src_ip",
            "dst_ip",
        ]

        for field in required_fields:
            value = result.get(field)

            if value is None or value == "":
                missing_fields.append(field)

        # -------------------------
        # Preprocess status
        # -------------------------

        if missing_fields:
            result["preprocess_status"] = "partial"
            result["processing_action"] = "keep"
            result["reason"] = (
                "missing required fields: "
                + ", ".join(missing_fields)
            )
        else:
            result["preprocess_status"] = "valid"
            result["processing_action"] = "normalized"

        return result