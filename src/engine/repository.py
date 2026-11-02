import ipaddress
from typing import Dict, Iterable, List, Set, Tuple

from src.engine.header_matcher import HeaderMatcher


class RuleRepository:
    def __init__(self) -> None:
        self._rules: List[Dict[str, object]] = []
        self._address_indexes: Dict[
            Tuple[str, str],
            Dict[Tuple[int, int], Set[int]],
        ] = {}
        self._wildcard_indexes: Dict[Tuple[str, str], Set[int]] = {}
        self._header_matcher = HeaderMatcher()

    def add_rule(self, rule: Dict[str, object]) -> None:
        if rule.get("status") != "valid":
            return

        header_fields = rule.get("header_fields")
        if not isinstance(header_fields, dict):
            return

        protocol = header_fields.get("protocol")
        if protocol not in {"tcp", "udp"}:
            return

        rule_index = len(self._rules)
        self._rules.append(rule)
        self._index_orientation(
            rule_index,
            protocol,
            header_fields["src_ip"],
            header_fields["dst_ip"],
        )

        if header_fields.get("direction") == "<>":
            self._index_orientation(
                rule_index,
                protocol,
                header_fields["dst_ip"],
                header_fields["src_ip"],
            )

    def add_rules(self, rules: Iterable[Dict[str, object]]) -> None:
        for rule in rules:
            self.add_rule(rule)

    def get_candidates(self, event: Dict[str, object]) -> List[Dict[str, object]]:
        protocol = str(event.get("protocol", "")).lower()
        if protocol not in {"tcp", "udp"}:
            return []

        try:
            source_ip = int(ipaddress.IPv4Address(event["src_ip"]))
            destination_ip = int(ipaddress.IPv4Address(event["dst_ip"]))
        except (KeyError, ipaddress.AddressValueError, TypeError):
            return []

        source_candidates = self._rules_for_address(
            protocol,
            "src_ip",
            source_ip,
        )
        destination_candidates = self._rules_for_address(
            protocol,
            "dst_ip",
            destination_ip,
        )
        possible_indexes = source_candidates & destination_candidates

        return [
            self._rules[index]
            for index in sorted(possible_indexes)
            if self._header_matcher.matches(
                self._rules[index]["header_fields"],
                event,
            )
        ]

    def _index_orientation(
        self,
        rule_index: int,
        protocol: str,
        source_selector: Dict[str, object],
        destination_selector: Dict[str, object],
    ) -> None:
        self._index_address(
            rule_index,
            protocol,
            "src_ip",
            source_selector,
        )
        self._index_address(
            rule_index,
            protocol,
            "dst_ip",
            destination_selector,
        )

    def _index_address(
        self,
        rule_index: int,
        protocol: str,
        field: str,
        selector: Dict[str, object],
    ) -> None:
        index_key = (protocol, field)

        if selector["type"] == "any":
            self._wildcard_indexes.setdefault(index_key, set()).add(rule_index)
            return

        network = ipaddress.IPv4Network(selector["value"])
        address_key = (int(network.network_address), network.prefixlen)
        address_index = self._address_indexes.setdefault(index_key, {})
        address_index.setdefault(address_key, set()).add(rule_index)

    def _rules_for_address(
        self,
        protocol: str,
        field: str,
        address: int,
    ) -> Set[int]:
        index_key = (protocol, field)
        matches = set(self._wildcard_indexes.get(index_key, set()))
        address_index = self._address_indexes.get(index_key, {})

        for prefix_length in range(33):
            mask = (
                0
                if prefix_length == 0
                else (0xFFFFFFFF << (32 - prefix_length)) & 0xFFFFFFFF
            )
            network_key = (address & mask, prefix_length)
            matches.update(address_index.get(network_key, set()))

        return matches
