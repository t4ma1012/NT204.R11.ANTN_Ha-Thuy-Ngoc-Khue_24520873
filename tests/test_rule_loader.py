import json
from pathlib import Path

from src.engine.rule_loader import RuleLoader


def test_load_file_skips_comments_and_blank_lines():
    project_root = Path(__file__).resolve().parents[1]
    input_path = project_root / "TEST" / "BT3" / "T01" / "input.rules"
    output_path = project_root / "TEST" / "BT3" / "T01" / "output.json"
    parser_inputs = []

    def parse_rule(rule_text):
        parser_inputs.append(rule_text)
        return {"rule_text": rule_text}

    rules = RuleLoader().load_file(input_path, parse_rule)

    assert parser_inputs == [
        'alert tcp any any -> any 80 (msg:"HTTP traffic"; sid:1000001; rev:1;)',
        'alert udp any any -> any 53 (msg:"DNS traffic"; sid:1000002; rev:1;)',
    ]
    assert rules == [{"rule_text": rule_text} for rule_text in parser_inputs]

    output_path.write_text(
        json.dumps(
            {
                "parser_inputs": parser_inputs,
                "loaded_rules": rules,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
