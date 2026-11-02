from typing import Dict


class PacketMatcher:
    def matches(self, rule: Dict[str, object], event: Dict[str, object]) -> bool:
        flags_condition = rule.get("flags_condition")
        dsize_condition = rule.get("dsize_condition")
        if flags_condition is None and dsize_condition is None:
            return True

        if flags_condition is not None:
            if str(event.get("protocol", "")).lower() != "tcp":
                return False
            if not self._matches_flags(flags_condition, event.get("flags")):
                return False

        if dsize_condition is not None and not self._matches_dsize(
            dsize_condition,
            event.get("payload_length"),
        ):
            return False

        return True

    @staticmethod
    def _matches_flags(condition: object, event_flags: object) -> bool:
        if not isinstance(condition, dict) or not isinstance(event_flags, str):
            return False

        flag_set = set(event_flags)
        if any(flag not in set("FSRPAU") for flag in flag_set):
            return False

        operator = condition.get("operator")
        if operator == "zero":
            return not flag_set
        if operator == "none":
            forbidden = condition.get("forbidden")
            return isinstance(forbidden, str) and flag_set.isdisjoint(forbidden)
        if operator == "any":
            required_any = condition.get("any")
            return (
                isinstance(required_any, str)
                and bool(required_any)
                and not flag_set.isdisjoint(required_any)
            )
        if operator == "all":
            required = condition.get("required")
            return (
                isinstance(required, str)
                and bool(required)
                and flag_set.issuperset(required)
            )
        return False

    @staticmethod
    def _matches_dsize(condition: object, payload_length: object) -> bool:
        if (
            not isinstance(condition, dict)
            or type(payload_length) is not int
            or payload_length < 0
        ):
            return False

        operator = condition.get("operator")
        value = condition.get("value")
        if operator == "exact":
            return type(value) is int and payload_length == value
        if operator == ">":
            return type(value) is int and payload_length > value
        if operator == "<":
            return type(value) is int and payload_length < value
        if operator == "range":
            minimum = condition.get("minimum")
            maximum = condition.get("maximum")
            return (
                type(minimum) is int
                and type(maximum) is int
                and minimum <= payload_length <= maximum
            )
        return False
