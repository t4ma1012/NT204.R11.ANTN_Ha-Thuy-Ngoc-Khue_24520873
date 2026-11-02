from typing import Dict, List, Optional, Tuple


class ContentMatcher:
    def matches(
        self,
        rule: Dict[str, object],
        event: Dict[str, object],
    ) -> Dict[str, object]:
        contents = rule.get("content_conditions", [])
        if not contents:
            return {"matched": True, "match_info": []}
        if not isinstance(contents, list):
            return {"matched": False, "match_info": []}

        fields = self._content_fields(event)
        match_info = []

        for content in contents:
            if not isinstance(content, dict):
                return {"matched": False, "match_info": []}
            pattern = content.get("pattern")
            nocase = content.get("nocase", False)
            if (
                not isinstance(pattern, str)
                or not pattern
                or not isinstance(nocase, bool)
            ):
                return {"matched": False, "match_info": []}
            offset = content.get("offset")
            if offset is None:
                offset = 0
            depth = content.get("depth")
            found = None

            for field_name, value in fields:
                if self._contains(value, pattern, nocase, offset, depth):
                    found = {
                        "content": pattern,
                        "field": field_name,
                        "nocase": nocase,
                    }
                    if content.get("offset") is not None:
                        found["offset"] = content["offset"]
                    if depth is not None:
                        found["depth"] = depth
                    break

            if found is None:
                return {"matched": False, "match_info": []}

            match_info.append(found)

        return {"matched": True, "match_info": match_info}

    @staticmethod
    def _content_fields(event: Dict[str, object]) -> List[Tuple[str, str]]:
        fields = []
        payload = event.get("payload")
        if isinstance(payload, str):
            fields.append(("payload", payload))

        application = event.get("application")
        if isinstance(application, dict):
            ContentMatcher._collect_strings(application, "application", fields)

        return fields

    @staticmethod
    def _collect_strings(
        value: object,
        field_path: str,
        fields: List[Tuple[str, str]],
    ) -> None:
        if isinstance(value, str):
            fields.append((field_path, value))
        elif isinstance(value, dict):
            for key, child in value.items():
                ContentMatcher._collect_strings(
                    child,
                    f"{field_path}.{key}",
                    fields,
                )
        elif isinstance(value, list):
            for index, child in enumerate(value):
                ContentMatcher._collect_strings(
                    child,
                    f"{field_path}[{index}]",
                    fields,
                )

    @staticmethod
    def _contains(
        value: str,
        pattern: str,
        nocase: bool,
        offset: int = 0,
        depth: Optional[int] = None,
    ) -> bool:
        if not isinstance(value, str) or not isinstance(pattern, str):
            return False
        if type(offset) is not int or offset < 0:
            return False
        if depth is not None and (type(depth) is not int or depth <= 0):
            return False

        pattern_end = len(pattern)
        byte_positions = [0]
        for character in value:
            byte_positions.append(
                byte_positions[-1] + len(character.encode("utf-8"))
            )

        region_end = (
            byte_positions[-1]
            if depth is None
            else offset + depth
        )
        for start in range(len(value) - pattern_end + 1):
            start_byte = byte_positions[start]
            end_byte = byte_positions[start + pattern_end]
            if start_byte < offset or end_byte > region_end:
                continue

            candidate = value[start : start + pattern_end]
            if nocase:
                if candidate.casefold() == pattern.casefold():
                    return True
            elif candidate == pattern:
                return True

        return False
