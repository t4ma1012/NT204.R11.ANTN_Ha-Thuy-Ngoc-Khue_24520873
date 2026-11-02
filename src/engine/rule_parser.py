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

        option_keywords, reason = self._extract_option_keywords(options)

        if reason is not None:
            return self._result(rule_text, "invalid", reason)

        unsupported = [
            keyword
            for keyword in option_keywords
            if keyword not in self.SUPPORTED_OPTIONS
        ]

        if unsupported:
            return self._result(
                rule_text,
                "unsupported",
                f"unsupported keyword '{unsupported[0]}'",
                header,
                options.strip(),
            )

        return {
            "status": "valid",
            "rule_text": rule_text,
            "header": header,
            "options": options.strip(),
            "reason": None,
        }

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
    def _extract_option_keywords(
        options: str,
    ) -> Tuple[List[str], Optional[str]]:
        keywords: List[str] = []
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

            keyword, separator, _ = option.partition(":")

            if not separator and keyword != "nocase":
                return [], f"malformed rule option '{keyword}'"

            if not keyword.isidentifier():
                return [], f"malformed rule option name '{keyword}'"

            keywords.append(keyword)

        return keywords, None

    @staticmethod
    def _result(
        rule_text: str,
        status: str,
        reason: str,
        header: Optional[str] = None,
        options: Optional[str] = None,
    ) -> Dict[str, object]:
        return {
            "status": status,
            "rule_text": rule_text,
            "header": header,
            "options": options,
            "reason": reason,
        }
