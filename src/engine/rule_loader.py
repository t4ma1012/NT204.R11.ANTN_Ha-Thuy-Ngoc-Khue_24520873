from pathlib import Path
from typing import Callable, List, TypeVar, Union


Rule = TypeVar("Rule")


class RuleLoader:
    def load_file(
        self,
        path: Union[str, Path],
        parse_rule: Callable[[str], Rule],
    ) -> List[Rule]:
        parsed_rules = []

        with Path(path).open("r", encoding="utf-8") as rule_file:
            for line in rule_file:
                rule_text = line.strip()

                if not rule_text or rule_text.startswith("#"):
                    continue

                parsed_rules.append(parse_rule(rule_text))

        return parsed_rules
