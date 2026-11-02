import ipaddress
from typing import Dict, List, Optional, Tuple


class RuleParser:
    SUPPORTED_OPTIONS = {
        "classtype",
        "content",
        "depth",
        "distance",
        "dsize",
        "flags",
        "flow",
        "msg",
        "nocase",
        "offset",
        "priority",
        "rev",
        "sid",
        "within",
    }

    def parse(self, rule_text: str) -> Dict[str, object]:
        rule_text = rule_text.strip()
        header, options, reason = self._split_rule(rule_text)

        if reason is not None:
            return self._result(rule_text, "invalid", reason)

        if not header or not options.strip():
            return self._result(
                rule_text,
                "invalid",
                "rule must contain a header and a non-empty options block",
            )

        header_fields, header_status, reason = self._parse_header(header)

        if reason is not None:
            return self._result(
                rule_text,
                header_status,
                reason,
                header,
                header_fields=header_fields,
            )

        parsed_options, reason = self._extract_options(options)

        if reason is not None:
            return self._result(
                rule_text,
                "invalid",
                reason,
                header,
                header_fields=header_fields,
            )

        unsupported = [
            keyword
            for keyword, _ in parsed_options
            if keyword not in self.SUPPORTED_OPTIONS
        ]

        if unsupported:
            return self._result(
                rule_text,
                "unsupported",
                f"unsupported keyword '{unsupported[0]}'",
                header,
                options.strip(),
                header_fields,
            )

        flow_values = [
            value for keyword, value in parsed_options if keyword == "flow"
        ]
        if len(flow_values) > 1:
            return self._result(
                rule_text,
                "invalid",
                "rule cannot contain multiple flow options",
                header,
                options.strip(),
                header_fields,
            )

        flow_conditions = None
        if flow_values:
            flow_value = flow_values[0]
            if not flow_value:
                return self._result(
                    rule_text,
                    "invalid",
                    "flow option requires at least one condition",
                    header,
                    options.strip(),
                    header_fields,
                )

            flow_conditions = [
                condition.strip() for condition in flow_value.split(",")
            ]
            if any(not condition for condition in flow_conditions):
                return self._result(
                    rule_text,
                    "invalid",
                    "flow option contains an empty condition",
                    header,
                    options.strip(),
                    header_fields,
                )

            unsupported_flow_conditions = [
                condition
                for condition in flow_conditions
                if condition
                not in {
                    "to_server",
                    "to_client",
                    "established",
                    "not_established",
                }
            ]
            if unsupported_flow_conditions:
                return self._result(
                    rule_text,
                    "unsupported",
                    "unsupported flow condition "
                    f"'{unsupported_flow_conditions[0]}'",
                    header,
                    options.strip(),
                    header_fields,
                )

        flag_values = [
            value for keyword, value in parsed_options if keyword == "flags"
        ]
        if len(flag_values) > 1:
            return self._result(
                rule_text,
                "invalid",
                "rule cannot contain multiple flags options",
                header,
                options.strip(),
                header_fields,
            )
        flags_condition = None
        if flag_values:
            flags_condition, reason = self._parse_flags(flag_values[0])
            if reason is not None:
                return self._result(
                    rule_text,
                    "invalid",
                    reason,
                    header,
                    options.strip(),
                    header_fields,
                )

        dsize_values = [
            value for keyword, value in parsed_options if keyword == "dsize"
        ]
        if len(dsize_values) > 1:
            return self._result(
                rule_text,
                "invalid",
                "rule cannot contain multiple dsize options",
                header,
                options.strip(),
                header_fields,
            )
        dsize_condition = None
        if dsize_values:
            dsize_condition, reason = self._parse_dsize(dsize_values[0])
            if reason is not None:
                return self._result(
                    rule_text,
                    "invalid",
                    reason,
                    header,
                    options.strip(),
                    header_fields,
                )

        rule_metadata: Dict[str, object] = {}
        for keyword in ("sid", "rev", "msg", "priority", "classtype"):
            values = [
                value
                for option_name, value in parsed_options
                if option_name == keyword
            ]
            if len(values) > 1:
                return self._result(
                    rule_text,
                    "invalid",
                    f"rule cannot contain multiple {keyword} options",
                    header,
                    options.strip(),
                    header_fields,
                )
            if not values:
                continue

            value = values[0]
            if value is None:
                return self._result(
                    rule_text,
                    "invalid",
                    f"{keyword} option requires a value",
                    header,
                    options.strip(),
                    header_fields,
                )
            if keyword in {"sid", "rev", "priority"}:
                if not value.isdecimal():
                    return self._result(
                        rule_text,
                        "invalid",
                        f"{keyword} option requires a non-negative integer",
                        header,
                        options.strip(),
                        header_fields,
                    )
                rule_metadata[keyword] = int(value)
            else:
                rule_metadata[keyword] = value

        content_conditions: List[Dict[str, object]] = []
        for keyword, value in parsed_options:
            if keyword == "content":
                if value is None:
                    return self._result(
                        rule_text,
                        "invalid",
                        "content option requires a quoted pattern",
                        header,
                        options.strip(),
                        header_fields,
                    )

                content_conditions.append(
                    {
                        "pattern": value,
                        "nocase": False,
                        "offset": None,
                        "depth": None,
                        "distance": None,
                        "within": None,
                    }
                )
            elif keyword == "nocase":
                if not content_conditions:
                    return self._result(
                        rule_text,
                        "invalid",
                        "nocase option must follow a content option",
                        header,
                        options.strip(),
                        header_fields,
                    )
                content_conditions[-1]["nocase"] = True
            elif keyword in {"offset", "depth", "distance", "within"}:
                if not content_conditions:
                    return self._result(
                        rule_text,
                        "invalid",
                        f"{keyword} option must follow a content option",
                        header,
                        options.strip(),
                        header_fields,
                    )
                if keyword in {"distance", "within"} and len(content_conditions) < 2:
                    return self._result(
                        rule_text,
                        "invalid",
                        f"{keyword} option requires a preceding content option",
                        header,
                        options.strip(),
                        header_fields,
                    )
                if value is None or not value.isdecimal():
                    requirement = (
                        "a positive integer"
                        if keyword in {"depth", "within"}
                        else "a non-negative integer"
                    )
                    return self._result(
                        rule_text,
                        "invalid",
                        f"{keyword} option requires {requirement}",
                        header,
                        options.strip(),
                        header_fields,
                    )
                number = int(value)
                if keyword in {"depth", "within"} and number == 0:
                    return self._result(
                        rule_text,
                        "invalid",
                        f"{keyword} option requires a positive integer",
                        header,
                        options.strip(),
                        header_fields,
                    )
                if content_conditions[-1][keyword] is not None:
                    return self._result(
                        rule_text,
                        "invalid",
                        f"content cannot contain multiple {keyword} options",
                        header,
                        options.strip(),
                        header_fields,
                    )
                content_conditions[-1][keyword] = number

        rule = {
            "status": "valid",
            "rule_text": rule_text,
            "header": header,
            "header_fields": header_fields,
            "options": options.strip(),
            "reason": None,
        }
        if flow_conditions is not None:
            rule["flow_conditions"] = flow_conditions
        if flags_condition is not None:
            rule["flags_condition"] = flags_condition
        if dsize_condition is not None:
            rule["dsize_condition"] = dsize_condition
        if rule_metadata:
            rule["metadata"] = rule_metadata
        if content_conditions:
            rule["content_conditions"] = content_conditions

        return rule

    @staticmethod
    def _parse_flags(value: Optional[str]) -> Tuple[Optional[Dict[str, object]], Optional[str]]:
        valid_flags = set("FSRPAU")
        if not value:
            return None, "flags option requires at least one TCP flag"

        operator = "all"
        flags_text = value
        if flags_text[0] in {"!", "+"}:
            operator = "none" if flags_text[0] == "!" else "all"
            flags_text = flags_text[1:]
        elif "*" in flags_text:
            if flags_text.count("*") != 1 or not flags_text.endswith("*"):
                return None, "flags option has an invalid wildcard modifier"
            operator = "any"
            flags_text = flags_text[:-1]

        if flags_text == "0":
            if operator != "all":
                return None, "flags option cannot combine 0 with a modifier"
            return {"required": "", "forbidden": "", "operator": "zero"}, None
        if not flags_text or any(flag not in valid_flags for flag in flags_text):
            return None, "flags option contains an unsupported TCP flag"
        if len(set(flags_text)) != len(flags_text):
            return None, "flags option contains duplicate TCP flags"

        return {
            "required": flags_text if operator == "all" else "",
            "forbidden": flags_text if operator == "none" else "",
            "any": flags_text if operator == "any" else "",
            "operator": operator,
        }, None

    @staticmethod
    def _parse_dsize(value: Optional[str]) -> Tuple[Optional[Dict[str, object]], Optional[str]]:
        if not value:
            return None, "dsize option requires a size condition"

        if value.startswith(">") or value.startswith("<"):
            operator = value[0]
            operand = value[1:]
            if not operand.isdecimal():
                return None, "dsize comparison requires a non-negative integer"
            return {"operator": operator, "value": int(operand)}, None

        if "<>" in value:
            parts = value.split("<>")
            if (
                len(parts) != 2
                or not parts[0].isdecimal()
                or not parts[1].isdecimal()
            ):
                return None, "dsize range must use non-negative min<>max values"
            minimum, maximum = map(int, parts)
            if minimum > maximum:
                return None, "dsize range minimum cannot exceed maximum"
            return {
                "operator": "range",
                "minimum": minimum,
                "maximum": maximum,
            }, None

        if not value.isdecimal():
            return None, "dsize requires an integer, comparison, or range"
        return {"operator": "exact", "value": int(value)}, None

    def _parse_header(
        self,
        header: str,
    ) -> Tuple[Optional[Dict[str, object]], str, Optional[str]]:
        fields = header.split()

        if len(fields) != 7:
            return None, "invalid", "rule header must contain seven fields"

        action, protocol, source_ip, source_port, direction, dest_ip, dest_port = (
            fields
        )

        if action != "alert":
            return None, "unsupported", f"unsupported rule action '{action}'"

        protocol = protocol.lower()
        if protocol not in {"tcp", "udp"}:
            return (
                None,
                "unsupported",
                f"unsupported protocol '{protocol}'",
            )

        source_address, reason = self._parse_address(source_ip)
        if reason is not None:
            return None, "invalid", f"invalid source IP: {reason}"

        destination_address, reason = self._parse_address(dest_ip)
        if reason is not None:
            return None, "invalid", f"invalid destination IP: {reason}"

        source_port_range, reason = self._parse_port(source_port)
        if reason is not None:
            return None, "invalid", f"invalid source port: {reason}"

        destination_port_range, reason = self._parse_port(dest_port)
        if reason is not None:
            return None, "invalid", f"invalid destination port: {reason}"

        if direction not in {"->", "<>"}:
            return None, "invalid", f"invalid rule direction '{direction}'"

        return {
            "action": action,
            "protocol": protocol,
            "src_ip": source_address,
            "src_port": source_port_range,
            "direction": direction,
            "dst_ip": destination_address,
            "dst_port": destination_port_range,
        }, "valid", None

    @staticmethod
    def _parse_address(
        value: str,
    ) -> Tuple[Optional[Dict[str, object]], Optional[str]]:
        if value == "any":
            return {"type": "any"}, None

        try:
            network = ipaddress.ip_network(value, strict=False)
        except ValueError:
            return None, f"'{value}' is not a valid IPv4 address or CIDR"

        if not isinstance(network, ipaddress.IPv4Network):
            return None, f"'{value}' is not an IPv4 address or CIDR"

        return {"type": "network", "value": str(network)}, None

    @staticmethod
    def _parse_port(
        value: str,
    ) -> Tuple[Optional[Dict[str, object]], Optional[str]]:
        if value == "any":
            return {"type": "any"}, None

        parts = value.split(":")
        if len(parts) > 2 or any(not part.isdecimal() for part in parts):
            return None, f"'{value}' is not a port or port range"

        start = int(parts[0])
        end = int(parts[-1])

        if not 0 <= start <= 65535 or not 0 <= end <= 65535:
            return None, f"'{value}' is outside the valid port range 0-65535"

        if start > end:
            return None, f"'{value}' has a descending port range"

        return {
            "type": "single" if len(parts) == 1 else "range",
            "start": start,
            "end": end,
        }, None

    def _split_rule(
        self,
        rule_text: str,
    ) -> Tuple[str, str, Optional[str]]:
        quoted = False
        escaped = False
        opening = None

        for index, character in enumerate(rule_text):
            if escaped:
                escaped = False
                continue

            if quoted and character == "\\":
                escaped = True
                continue

            if character == '"':
                quoted = not quoted
            elif character == "(" and not quoted:
                opening = index
                break

        if opening is None:
            return "", "", "missing opening '(' for rule options"

        quoted = False
        escaped = False
        depth = 0

        for index in range(opening, len(rule_text)):
            character = rule_text[index]

            if escaped:
                escaped = False
                continue

            if quoted and character == "\\":
                escaped = True
                continue

            if character == '"':
                quoted = not quoted
            elif not quoted and character == "(":
                depth += 1
            elif not quoted and character == ")":
                depth -= 1

                if depth == 0:
                    if rule_text[index + 1 :].strip():
                        return "", "", "unexpected text after rule options"

                    return (
                        rule_text[:opening].strip(),
                        rule_text[opening + 1 : index],
                        None,
                    )

        if quoted:
            return "", "", "unterminated quoted string in rule options"

        return "", "", "missing closing ')' for rule options"

    @staticmethod
    def _extract_options(
        options: str,
    ) -> Tuple[List[Tuple[str, Optional[str]]], Optional[str]]:
        parsed_options: List[Tuple[str, Optional[str]]] = []
        current = []
        quoted = False
        escaped = False
        option_parts = []

        for character in options:
            if escaped:
                current.append(character)
                escaped = False
                continue

            if quoted and character == "\\":
                current.append(character)
                escaped = True
                continue

            if character == '"':
                quoted = not quoted
                current.append(character)
            elif character == ";" and not quoted:
                option_parts.append("".join(current).strip())
                current = []
            else:
                current.append(character)

        if quoted:
            return [], "unterminated quoted string in rule options"

        option_parts.append("".join(current).strip())

        for option in option_parts:
            if not option:
                continue

            keyword, separator, option_value = option.partition(":")

            if not separator and keyword != "nocase":
                return [], f"malformed rule option '{keyword}'"

            if not keyword.isidentifier():
                return [], f"malformed rule option name '{keyword}'"

            value = option_value.strip() if separator else None
            if keyword == "content" and value is not None:
                if (
                    len(value) < 2
                    or not value.startswith('"')
                    or not value.endswith('"')
                ):
                    return [], "content option requires a quoted pattern"
                value = value[1:-1]
                if not value:
                    return [], "content option requires a non-empty pattern"
            elif (
                keyword not in {"offset", "depth", "distance", "within"}
                and value
                and value.startswith('"')
                and value.endswith('"')
            ):
                value = value[1:-1]

            parsed_options.append((keyword, value))

        return parsed_options, None

    @staticmethod
    def _result(
        rule_text: str,
        status: str,
        reason: str,
        header: Optional[str] = None,
        options: Optional[str] = None,
        header_fields: Optional[Dict[str, object]] = None,
    ) -> Dict[str, object]:
        return {
            "status": status,
            "rule_text": rule_text,
            "header": header,
            "header_fields": header_fields,
            "options": options,
            "reason": reason,
        }
