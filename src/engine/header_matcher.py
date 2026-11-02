import ipaddress
from typing import Dict


class HeaderMatcher:
    def matches(
        self,
        header_fields: Dict[str, object],
        event: Dict[str, object],
    ) -> bool:
        if (
            str(event.get("protocol", "")).lower()
            != header_fields.get("protocol")
        ):
            return False

        direct = self._matches_orientation(
            header_fields,
            event.get("src_ip"),
            event.get("src_port"),
            event.get("dst_ip"),
            event.get("dst_port"),
        )

        if direct or header_fields.get("direction") == "->":
            return direct

        if header_fields.get("direction") == "<>":
            return self._matches_orientation(
                header_fields,
                event.get("dst_ip"),
                event.get("dst_port"),
                event.get("src_ip"),
                event.get("src_port"),
            )

        return False

    @classmethod
    def _matches_orientation(
        cls,
        header_fields: Dict[str, object],
        src_ip: object,
        src_port: object,
        dst_ip: object,
        dst_port: object,
    ) -> bool:
        return (
            cls._matches_address(header_fields["src_ip"], src_ip)
            and cls._matches_port(header_fields["src_port"], src_port)
            and cls._matches_address(header_fields["dst_ip"], dst_ip)
            and cls._matches_port(header_fields["dst_port"], dst_port)
        )

    @staticmethod
    def _matches_address(selector: Dict[str, object], value: object) -> bool:
        if selector["type"] == "any":
            return True

        try:
            address = ipaddress.ip_address(value)
            network = ipaddress.ip_network(selector["value"])
        except (TypeError, ValueError):
            return False

        return address in network

    @staticmethod
    def _matches_port(selector: Dict[str, object], value: object) -> bool:
        if selector["type"] == "any":
            return True

        try:
            port = int(value)
        except (TypeError, ValueError):
            return False

        return selector["start"] <= port <= selector["end"]
