from typing import Dict, List, Tuple


class ContentMatcher:
    def matches(
        self,
        rule: Dict[str, object],
        event: Dict[str, object],
    ) -> Dict[str, object]:
        contents = rule.get("content_conditions", [])
        if not contents:
            return {"matched": True, "match_info": []}

        fields = self._content_fields(event)
        match_info = []

        for content in contents:
            pattern = content["pattern"]
            nocase = content["nocase"]
            found = None

            for field_name, value in fields:
                if self._contains(value, pattern, nocase):
                    found = {
                        "content": pattern,
                        "field": field_name,
                        "nocase": nocase,
                    }
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
    def _contains(value: str, pattern: str, nocase: bool) -> bool:
        if nocase:
            return pattern.casefold() in value.casefold()
        return pattern in value
