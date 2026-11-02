import logging
from pathlib import Path
from typing import Callable, List, TypeVar, Union


logger = logging.getLogger(__name__)

Rule = TypeVar("Rule")


class RuleLoader:
    def load_file(
        self,
        path: Union[str, Path],
        parse_rule: Callable[[str], Rule],
    ) -> List[Rule]:
        parsed_rules = []

        with Path(path).open("r", encoding="utf-8") as rule_file:
            for line_number, line in enumerate(rule_file, start=1):
                rule_text = line.strip()

                if not rule_text or rule_text.startswith("#"):
                    continue

                try:
                    parsed_rule = parse_rule(rule_text)
                except ValueError as error:
                    parsed_rule = {
                        "status": "invalid",
                        "rule_text": rule_text,
                        "header": None,
                        "options": None,
                        "reason": str(error),
                    }

                if (
                    isinstance(parsed_rule, dict)
                    and parsed_rule.get("status") == "invalid"
                ):
                    logger.warning(
                        "Invalid rule at %s:%d: %s",
                        path,
                        line_number,
                        parsed_rule.get("reason", "invalid rule syntax"),
                    )

                parsed_rules.append(parsed_rule)

        return parsed_rules
