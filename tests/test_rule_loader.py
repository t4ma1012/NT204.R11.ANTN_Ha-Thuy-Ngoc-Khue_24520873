import json
from pathlib import Path

from src.engine.rule_loader import RuleLoader
from src.engine.header_matcher import HeaderMatcher
from src.engine.evaluator import RuleEvaluationEngine
from src.engine.rule_parser import RuleParser
from src.engine.repository import RuleRepository


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


def test_rule_direction_matches_forward_and_reverse_events():
    project_root = Path(__file__).resolve().parents[1]
    input_path = project_root / "TEST" / "BT3" / "T05" / "input.rules"
    output_path = project_root / "TEST" / "BT3" / "T05" / "output.json"

    rules = RuleLoader().load_file(input_path, RuleParser().parse)
    matcher = HeaderMatcher()
    forward_event = {
        "protocol": "tcp",
        "src_ip": "10.0.0.1",
        "src_port": 12345,
        "dst_ip": "10.0.0.2",
        "dst_port": 80,
    }
    reverse_event = {
        "protocol": "tcp",
        "src_ip": "10.0.0.2",
        "src_port": 80,
        "dst_ip": "10.0.0.1",
        "dst_port": 12345,
    }

    assert len(rules) == 2
    assert all(rule["status"] == "valid" for rule in rules)
    unidirectional, bidirectional = rules
    assert unidirectional["header_fields"]["direction"] == "->"
    assert bidirectional["header_fields"]["direction"] == "<>"

    actual_matches = {
        "unidirectional_forward": matcher.matches(
            unidirectional["header_fields"],
            forward_event,
        ),
        "unidirectional_reverse": matcher.matches(
            unidirectional["header_fields"],
            reverse_event,
        ),
        "bidirectional_forward": matcher.matches(
            bidirectional["header_fields"],
            forward_event,
        ),
        "bidirectional_reverse": matcher.matches(
            bidirectional["header_fields"],
            reverse_event,
        ),
    }

    assert actual_matches == {
        "unidirectional_forward": True,
        "unidirectional_reverse": False,
        "bidirectional_forward": True,
        "bidirectional_reverse": True,
    }

    output_path.write_text(
        json.dumps(
            {
                "directions": [
                    rule["header_fields"]["direction"] for rule in rules
                ],
                "matches": actual_matches,
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def test_repository_index_returns_matching_protocol_and_header_candidates():
    project_root = Path(__file__).resolve().parents[1]
    input_path = project_root / "TEST" / "BT3" / "T06" / "input.rules"
    output_path = project_root / "TEST" / "BT3" / "T06" / "output.json"

    rules = RuleLoader().load_file(input_path, RuleParser().parse)
    repository = RuleRepository()
    repository.add_rules(rules)

    events = {
        "tcp_cidr_and_wildcard": {
            "protocol": "TCP",
            "src_ip": "10.1.2.3",
            "src_port": 1500,
            "dst_ip": "192.0.2.20",
            "dst_port": 443,
        },
        "udp_wildcard": {
            "protocol": "UDP",
            "src_ip": "203.0.113.8",
            "src_port": 53000,
            "dst_ip": "192.0.2.53",
            "dst_port": 53,
        },
        "udp_cidr_and_port_ranges": {
            "protocol": "UDP",
            "src_ip": "10.1.2.3",
            "src_port": 1500,
            "dst_ip": "192.0.2.20",
            "dst_port": 5500,
        },
    }

    actual_candidates = {
        name: [
            rule["rule_text"]
            for rule in repository.get_candidates(event)
        ]
        for name, event in events.items()
    }

    assert actual_candidates == {
        "tcp_cidr_and_wildcard": [
            rules[0]["rule_text"],
            rules[1]["rule_text"],
        ],
        "udp_wildcard": [rules[3]["rule_text"]],
        "udp_cidr_and_port_ranges": [rules[4]["rule_text"]],
    }

    output_path.write_text(
        json.dumps(
            {
                name: [rule["rule_text"] for rule in repository.get_candidates(event)]
                for name, event in events.items()
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def test_header_mismatch_is_filtered_before_content_matching():
    project_root = Path(__file__).resolve().parents[1]
    input_path = project_root / "TEST" / "BT3" / "T07" / "input.rules"
    output_path = project_root / "TEST" / "BT3" / "T07" / "output.json"

    rules = RuleLoader().load_file(input_path, RuleParser().parse)
    content_checks = []
    generated_events = []

    def content_matcher(rule, event):
        content_checks.append(rule["rule_text"])
        return (
            '"MATCHME"' in rule["options"]
            and "MATCHME" in event["payload"]
        )

    def detection_event_generator(rule, event):
        detection_event = {
            "rule_text": rule["rule_text"],
            "src_ip": event["src_ip"],
            "dst_ip": event["dst_ip"],
        }
        generated_events.append(detection_event)
        return detection_event

    repository = RuleRepository()
    repository.add_rule(rules[0])
    evaluator = RuleEvaluationEngine(
        repository, content_matcher, detection_event_generator
    )
    matching_payload = "request contains MATCHME"
    mismatched_events = {
        "protocol": {
            "protocol": "UDP",
            "src_ip": "10.0.0.1",
            "src_port": 12345,
            "dst_ip": "10.0.0.2",
            "dst_port": 80,
            "payload": matching_payload,
        },
        "ip": {
            "protocol": "TCP",
            "src_ip": "198.51.100.10",
            "src_port": 12345,
            "dst_ip": "10.0.0.2",
            "dst_port": 80,
            "payload": matching_payload,
        },
        "port": {
            "protocol": "TCP",
            "src_ip": "10.0.0.1",
            "src_port": 12345,
            "dst_ip": "10.0.0.2",
            "dst_port": 443,
            "payload": matching_payload,
        },
    }

    mismatch_results = {
        mismatch: evaluator.evaluate(event)
        for mismatch, event in mismatched_events.items()
    }

    assert mismatch_results == {
        "protocol": [],
        "ip": [],
        "port": [],
    }
    assert content_checks == []
    assert generated_events == []

    matching_event = {
        "protocol": "TCP",
        "src_ip": "10.0.0.1",
        "src_port": 12345,
        "dst_ip": "10.0.0.2",
        "dst_port": 80,
        "payload": matching_payload,
    }
    matching_result = evaluator.evaluate(matching_event)

    assert matching_result == generated_events
    assert len(matching_result) == 1
    assert content_checks == [rules[0]["rule_text"]]

    output_path.write_text(
        json.dumps(
            {
                "mismatch_results": mismatch_results,
                "content_checks_after_mismatches": [],
                "detection_events_after_mismatches": [],
                "matching_header_detection_events": matching_result,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
