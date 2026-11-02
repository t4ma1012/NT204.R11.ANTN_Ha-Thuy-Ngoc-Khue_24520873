import json
from pathlib import Path

from src.engine.rule_loader import RuleLoader
from src.engine.rule_parser import RuleParser


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


def test_syntax_invalid_rule_does_not_stop_loading():
    project_root = Path(__file__).resolve().parents[1]
    input_path = project_root / "TEST" / "BT3" / "T02" / "input.rules"
    output_path = project_root / "TEST" / "BT3" / "T02" / "output.json"

    rules = RuleLoader().load_file(input_path, RuleParser().parse)

    assert len(rules) == 2
    assert rules[0]["status"] == "invalid"
    assert rules[0]["reason"] == "missing closing ')' for rule options"
    assert rules[1]["status"] == "valid"
    assert rules[1]["header"] == "alert udp any any -> any 53"
    assert rules[1]["options"] == (
        'msg:"Valid DNS rule"; sid:1000004; rev:1;'
    )

    output_path.write_text(
        json.dumps({"rules": rules}, indent=2),
        encoding="utf-8",
    )


def test_unsupported_keyword_does_not_stop_loading():
    project_root = Path(__file__).resolve().parents[1]
    input_path = project_root / "TEST" / "BT3" / "T03" / "input.rules"
    output_path = project_root / "TEST" / "BT3" / "T03" / "output.json"

    rules = RuleLoader().load_file(input_path, RuleParser().parse)

    assert len(rules) == 2
    assert rules[0]["status"] == "unsupported"
    assert rules[0]["reason"] == "unsupported keyword 'pcre'"
    assert rules[0]["header"] == "alert tcp any any -> any 80"
    assert rules[1]["status"] == "valid"
    assert rules[1]["header"] == "alert udp any any -> any 53"

    output_path.write_text(
        json.dumps({"rules": rules}, indent=2),
        encoding="utf-8",
    )


def test_tcp_header_parses_ip_and_port_fields():
    project_root = Path(__file__).resolve().parents[1]
    input_path = project_root / "TEST" / "BT3" / "T04" / "input.rules"
    output_path = project_root / "TEST" / "BT3" / "T04" / "output.json"

    rules = RuleLoader().load_file(input_path, RuleParser().parse)

    assert len(rules) == 3
    assert all(rule["status"] == "valid" for rule in rules)

    first, second, third = [
        rule["header_fields"] for rule in rules
    ]

    assert first["protocol"] == "tcp"
    assert first["src_ip"] == {"type": "any"}
    assert first["src_port"] == {"type": "any"}
    assert first["dst_ip"] == {
        "type": "network",
        "value": "192.0.2.10/32",
    }
    assert first["dst_port"] == {
        "type": "single",
        "start": 443,
        "end": 443,
    }

    assert second["src_ip"] == {
        "type": "network",
        "value": "10.10.0.0/16",
    }
    assert second["src_port"] == {
        "type": "range",
        "start": 1024,
        "end": 65535,
    }
    assert second["dst_ip"] == {"type": "any"}
    assert second["dst_port"] == {
        "type": "range",
        "start": 8000,
        "end": 8080,
    }

    assert third["src_ip"] == {
        "type": "network",
        "value": "198.51.100.25/32",
    }
    assert third["src_port"] == {
        "type": "single",
        "start": 22,
        "end": 22,
    }
    assert third["dst_ip"] == {
        "type": "network",
        "value": "203.0.113.0/24",
    }
    assert third["dst_port"] == {"type": "any"}

    output_path.write_text(
        json.dumps(
            {
                "status": [rule["status"] for rule in rules],
                "parsed_headers": [rule["header_fields"] for rule in rules],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
