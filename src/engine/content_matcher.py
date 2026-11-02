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
        if any(not self._valid_content(content) for content in contents):
            return {"matched": False, "match_info": []}

        for field_name, value in fields:
            match_info = self._match_sequence(contents, value, field_name)
            if match_info is not None:
                return {"matched": True, "match_info": match_info}

        return {"matched": False, "match_info": []}

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
    def _valid_content(content: object) -> bool:
        if not isinstance(content, dict):
            return False
        pattern = content.get("pattern")
        if (
            not isinstance(pattern, str)
            or not pattern
            or not isinstance(content.get("nocase", False), bool)
        ):
            return False
        for name, minimum in (
            ("offset", 0),
            ("depth", 1),
            ("distance", 0),
            ("within", 1),
        ):
            value = content.get(name)
            if value is not None and (
                type(value) is not int or value < minimum
            ):
                return False
        return True

    @classmethod
    def _match_sequence(
        cls,
        contents: List[Dict[str, object]],
        value: str,
        field_name: str,
    ) -> Optional[List[Dict[str, object]]]:
        if contents[0].get("distance") is not None or contents[0].get(
            "within"
        ) is not None:
            return None

        byte_positions = [0]
        for character in value:
            byte_positions.append(
                byte_positions[-1] + len(character.encode("utf-8"))
            )

        def find_next(
            index: int,
            previous_end: Optional[int],
            info: List[Dict[str, object]],
        ) -> Optional[List[Dict[str, object]]]:
            if index == len(contents):
                return info

            content = contents[index]
            offset = content.get("offset")
            depth = content.get("depth")
            distance = content.get("distance")
            within = content.get("within")

            minimum_start = offset or 0
            if previous_end is not None and distance is not None:
                minimum_start = max(minimum_start, previous_end + distance)
            elif previous_end is not None and within is not None:
                minimum_start = max(minimum_start, previous_end)

            maximum_end = None
            if depth is not None:
                maximum_end = (offset or 0) + depth
            if previous_end is not None and within is not None:
                relative_end = previous_end + within
                maximum_end = (
                    relative_end
                    if maximum_end is None
                    else min(maximum_end, relative_end)
                )

            matches = cls._find_matches(
                value,
                content["pattern"],
                content.get("nocase", False),
                byte_positions,
                minimum_start,
                maximum_end,
            )
            for start, end in matches:
                item = {
                    "content": content["pattern"],
                    "field": field_name,
                    "nocase": content.get("nocase", False),
                }
                for modifier in ("offset", "depth", "distance", "within"):
                    if content.get(modifier) is not None:
                        item[modifier] = content[modifier]

                result = find_next(index + 1, end, info + [item])
                if result is not None:
                    return result
            return None

        return find_next(0, None, [])

    @staticmethod
    def _find_matches(
        value: str,
        pattern: str,
        nocase: bool,
        byte_positions: List[int],
        minimum_start: int,
        maximum_end: Optional[int],
    ) -> List[Tuple[int, int]]:
        found = []
        pattern_to_match = pattern.casefold() if nocase else pattern

        for start_index in range(len(value)):
            start_byte = byte_positions[start_index]
            if start_byte < minimum_start:
                continue
            if maximum_end is not None and start_byte >= maximum_end:
                continue

            if nocase:
                max_end_index = min(
                    len(value),
                    start_index + max(1, len(pattern) * 3),
                )
            else:
                max_end_index = min(len(value), start_index + len(pattern))

            for end_index in range(start_index + 1, max_end_index + 1):
                end_byte = byte_positions[end_index]
                if maximum_end is not None and end_byte > maximum_end:
                    break

                candidate = value[start_index:end_index]
                candidate_to_match = candidate.casefold() if nocase else candidate
                if nocase and len(candidate_to_match) > len(pattern_to_match):
                    break
                if candidate_to_match == pattern_to_match:
                    found.append((start_byte, end_byte))

        return found

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
        byte_positions = [0]
        for character in value:
            byte_positions.append(
                byte_positions[-1] + len(character.encode("utf-8"))
            )
        return bool(
            ContentMatcher._find_matches(
                value,
                pattern,
                nocase,
                byte_positions,
                offset,
                None if depth is None else offset + depth,
            )
        )
