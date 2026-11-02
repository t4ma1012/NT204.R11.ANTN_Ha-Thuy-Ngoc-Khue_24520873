import json
from pathlib import Path

from src.engine.rule_loader import RuleLoader
from src.engine.header_matcher import HeaderMatcher
from src.engine.content_matcher import ContentMatcher
from src.engine.evaluator import RuleEvaluationEngine
from src.engine.rule_parser import RuleParser
from src.engine.repository import RuleRepository
from src.flow.tracker import FlowTracker


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


def test_content_distance_within_relative_matching():
    project_root = Path(__file__).resolve().parents[1]
    input_path = project_root / "TEST" / "BT3" / "T11" / "input.rules"
    output_path = project_root / "TEST" / "BT3" / "T11" / "output.json"

    parser = RuleParser()
    rules = RuleLoader().load_file(input_path, parser.parse)
    assert len(rules) == 1
    assert rules[0]["status"] == "valid"
    assert rules[0]["content_conditions"] == [
        {
            "pattern": "HEAD",
            "nocase": False,
            "offset": None,
            "depth": None,
            "distance": None,
            "within": None,
        },
        {
            "pattern": "TAIL",
            "nocase": False,
            "offset": 6,
            "depth": 6,
            "distance": 2,
            "within": 8,
        },
    ]

    repository = RuleRepository()
    repository.add_rules(rules)
    matcher = ContentMatcher()

    def detection_event_generator(rule, event):
        return {"rule_text": rule["rule_text"]}

    evaluator = RuleEvaluationEngine(
        repository,
        matcher.matches,
        detection_event_generator,
    )
    event_fields = {
        "protocol": "TCP",
        "src_ip": "10.0.0.1",
        "src_port": 51000,
        "dst_ip": "10.0.0.2",
        "dst_port": 80,
    }

    match_payloads = [
        "HEAD--TAIL",
        "HEAD---TAIL",
        "HEAD----TAIL",
    ]
    no_match_payloads = [
        "HEAD-TAIL",
        "HEAD------TAIL",
        "HEAD--------TAIL",
        "TAIL--HEAD",
    ]
    match_results = [
        evaluator.evaluate({**event_fields, "payload": payload})
        for payload in match_payloads
    ]
    no_match_results = [
        evaluator.evaluate({**event_fields, "payload": payload})
        for payload in no_match_payloads
    ]

    assert all(len(result) == 1 for result in match_results)
    assert all(result == [] for result in no_match_results)
    assert match_results[0][0]["match_info"][1] == {
        "content": "TAIL",
        "field": "payload",
        "nocase": False,
        "offset": 6,
        "depth": 6,
        "distance": 2,
        "within": 8,
    }
    distance_only_rule = {
        "content_conditions": [
            {"pattern": "HEAD", "nocase": False},
            {"pattern": "TAIL", "nocase": False, "distance": 2},
        ]
    }
    within_only_rule = {
        "content_conditions": [
            {"pattern": "HEAD", "nocase": False},
            {"pattern": "TAIL", "nocase": False, "within": 8},
        ]
    }
    independent_relative_results = {
        "distance_match": matcher.matches(
            distance_only_rule,
            {"payload": "HEAD--TAIL"},
        )["matched"],
        "distance_no_match": matcher.matches(
            distance_only_rule,
            {"payload": "HEAD-TAIL"},
        )["matched"],
        "within_match": matcher.matches(
            within_only_rule,
            {"payload": "HEAD----TAIL"},
        )["matched"],
        "within_no_match": matcher.matches(
            within_only_rule,
            {"payload": "HEAD------TAIL"},
        )["matched"],
    }
    assert independent_relative_results == {
        "distance_match": True,
        "distance_no_match": False,
        "within_match": True,
        "within_no_match": False,
    }

    invalid_rules = [
        'alert tcp any any -> any any (content:"HEAD"; distance:1; sid:1;)',
        'alert tcp any any -> any any (content:"HEAD"; content:"TAIL"; distance:-1; sid:2;)',
        'alert tcp any any -> any any (content:"HEAD"; content:"TAIL"; within:0; sid:3;)',
        'alert tcp any any -> any any (content:"HEAD"; content:"TAIL"; distance:"2"; sid:4;)',
    ]
    invalid_results = [parser.parse(rule) for rule in invalid_rules]
    assert all(result["status"] == "invalid" for result in invalid_results)
    assert matcher.matches(
        {
            "content_conditions": [
                {
                    "pattern": "HEAD",
                    "nocase": False,
                    "distance": 1,
                    "within": None,
                }
            ]
        },
        {**event_fields, "payload": "HEAD"},
    ) == {"matched": False, "match_info": []}

    output_path.write_text(
        json.dumps(
            {
                "match_payloads": [
                    {"payload": payload, "detections": result}
                    for payload, result in zip(match_payloads, match_results)
                ],
                "no_match_payloads": [
                    {"payload": payload, "detections": result}
                    for payload, result in zip(
                        no_match_payloads,
                        no_match_results,
                    )
                ],
                "independent_relative_results": independent_relative_results,
                "invalid_rule_statuses": [
                    {
                        "status": result["status"],
                        "reason": result["reason"],
                    }
                    for result in invalid_results
                ],
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


def test_flow_conditions_use_flow_tracker_context():
    project_root = Path(__file__).resolve().parents[1]
    input_path = project_root / "TEST" / "BT3" / "T08" / "input.rules"
    output_path = project_root / "TEST" / "BT3" / "T08" / "output.json"

    rules = RuleLoader().load_file(input_path, RuleParser().parse)
    assert all(rule["status"] == "valid" for rule in rules)
    assert rules[0]["flow_conditions"] == ["to_server", "established"]
    assert rules[1]["flow_conditions"] == ["to_client", "established"]
    assert rules[2]["flow_conditions"] == ["to_server", "not_established"]

    repository = RuleRepository()
    repository.add_rules(rules)
    generated_events = []

    def content_matcher(rule, event):
        return "FLOW" in event.get("payload", "")

    def detection_event_generator(rule, event):
        detection = {"rule_text": rule["rule_text"]}
        generated_events.append(detection)
        return detection

    evaluator = RuleEvaluationEngine(
        repository,
        content_matcher,
        detection_event_generator,
    )
    tracker = FlowTracker()
    handshake_events = [
        {
            "timestamp": 1,
            "protocol": "TCP",
            "src_ip": "10.0.0.1",
            "src_port": 51000,
            "dst_ip": "10.0.0.2",
            "dst_port": 80,
            "flags": "S",
            "payload_length": 0,
        },
        {
            "timestamp": 2,
            "protocol": "TCP",
            "src_ip": "10.0.0.2",
            "src_port": 80,
            "dst_ip": "10.0.0.1",
            "dst_port": 51000,
            "flags": "SA",
            "payload_length": 0,
        },
        {
            "timestamp": 3,
            "protocol": "TCP",
            "src_ip": "10.0.0.1",
            "src_port": 51000,
            "dst_ip": "10.0.0.2",
            "dst_port": 80,
            "flags": "A",
            "payload_length": 0,
        },
    ]
    for event in handshake_events:
        tracker.process(event)

    request_event = {
        "timestamp": 4,
        "protocol": "TCP",
        "src_ip": "10.0.0.1",
        "src_port": 51000,
        "dst_ip": "10.0.0.2",
        "dst_port": 80,
        "payload": "FLOW request",
    }
    request_context = tracker.process(
        {**request_event, "flags": "A", "payload_length": 12}
    ).to_context_dict()
    request_detections = evaluator.evaluate(request_event, request_context)

    response_event = {
        "timestamp": 5,
        "protocol": "TCP",
        "src_ip": "10.0.0.2",
        "src_port": 80,
        "dst_ip": "10.0.0.1",
        "dst_port": 51000,
        "payload": "FLOW response",
    }
    response_context = tracker.process(
        {**response_event, "flags": "A", "payload_length": 13}
    ).to_context_dict()
    response_detections = evaluator.evaluate(response_event, response_context)

    handshake_tracker = FlowTracker()
    handshake_context = handshake_tracker.process(
        handshake_events[0]
    ).to_context_dict()
    handshake_event = {
        **request_event,
        "timestamp": 6,
        "payload": "FLOW handshake",
    }
    handshake_detections = evaluator.evaluate(
        handshake_event,
        handshake_context,
    )
    missing_context_detections = evaluator.evaluate(handshake_event)

    assert request_context["tcp_state"] == "ESTABLISHED"
    assert request_context["direction"] == "to_server"
    assert [event["rule_text"] for event in request_detections] == [
        rules[0]["rule_text"]
    ]
    assert response_context["tcp_state"] == "ESTABLISHED"
    assert response_context["direction"] == "to_client"
    assert [event["rule_text"] for event in response_detections] == [
        rules[1]["rule_text"]
    ]
    assert handshake_context["tcp_state"] == "HANDSHAKE"
    assert handshake_context["direction"] == "to_server"
    assert [event["rule_text"] for event in handshake_detections] == [
        rules[2]["rule_text"]
    ]
    assert missing_context_detections == []
    assert generated_events == (
        request_detections + response_detections + handshake_detections
    )

    actual = {
        "established_request": {
            "tcp_state": request_context["tcp_state"],
            "direction": request_context["direction"],
            "matched_rules": [
                event["rule_text"] for event in request_detections
            ],
        },
        "established_response": {
            "tcp_state": response_context["tcp_state"],
            "direction": response_context["direction"],
            "matched_rules": [
                event["rule_text"] for event in response_detections
            ],
        },
        "not_established_request": {
            "tcp_state": handshake_context["tcp_state"],
            "direction": handshake_context["direction"],
            "matched_rules": [
                event["rule_text"] for event in handshake_detections
            ],
        },
        "missing_context_matches": missing_context_detections,
    }
    output_path.write_text(json.dumps(actual, indent=2), encoding="utf-8")


def test_content_matching_respects_nocase_and_reports_matched_field():
    project_root = Path(__file__).resolve().parents[1]
    input_path = project_root / "TEST" / "BT3" / "T09" / "input.rules"
    output_path = project_root / "TEST" / "BT3" / "T09" / "output.json"

    rules = RuleLoader().load_file(input_path, RuleParser().parse)
    assert all(rule["status"] == "valid" for rule in rules)
    assert rules[0]["content_conditions"] == [
        {
            "pattern": "Admin",
            "nocase": False,
            "offset": None,
            "depth": None,
            "distance": None,
            "within": None,
        }
    ]
    assert rules[1]["content_conditions"] == [
        {
            "pattern": "Admin",
            "nocase": True,
            "offset": None,
            "depth": None,
            "distance": None,
            "within": None,
        }
    ]

    repository = RuleRepository()
    repository.add_rules(rules)
    content_matcher = ContentMatcher()

    def detection_event_generator(rule, event):
        return {"rule_text": rule["rule_text"]}

    evaluator = RuleEvaluationEngine(
        repository,
        content_matcher.matches,
        detection_event_generator,
    )
    uppercase_event = {
        "protocol": "TCP",
        "src_ip": "10.0.0.1",
        "src_port": 51000,
        "dst_ip": "10.0.0.2",
        "dst_port": 80,
        "application": {"decoded_body": "ADMIN request"},
    }
    mixed_case_event = {
        **uppercase_event,
        "application": {"decoded_body": "Admin request"},
    }

    uppercase_matches = evaluator.evaluate(uppercase_event)
    mixed_case_matches = evaluator.evaluate(mixed_case_event)

    assert [event["rule_text"] for event in uppercase_matches] == [
        rules[1]["rule_text"]
    ]
    assert [event["rule_text"] for event in mixed_case_matches] == [
        rules[0]["rule_text"],
        rules[1]["rule_text"],
    ]
    assert uppercase_matches[0]["match_info"] == [
        {
            "content": "Admin",
            "field": "application.decoded_body",
            "nocase": True,
        }
    ]
    assert all(
        event["match_info"][0]["field"] == "application.decoded_body"
        for event in mixed_case_matches
    )

    output_path.write_text(
        json.dumps(
            {
                "uppercase_application_data": uppercase_matches,
                "mixed_case_application_data": mixed_case_matches,
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def test_content_offset_depth_limits_matching_region():
    project_root = Path(__file__).resolve().parents[1]
    input_path = project_root / "TEST" / "BT3" / "T10" / "input.rules"
    output_path = project_root / "TEST" / "BT3" / "T10" / "output.json"

    parser = RuleParser()
    rules = RuleLoader().load_file(input_path, parser.parse)
    assert all(rule["status"] == "valid" for rule in rules)
    assert rules[0]["content_conditions"] == [
        {
            "pattern": "ALERT",
            "nocase": False,
            "offset": 4,
            "depth": 6,
            "distance": None,
            "within": None,
        }
    ]
    assert rules[1]["content_conditions"] == [
        {
            "pattern": "TOKEN",
            "nocase": False,
            "offset": None,
            "depth": 5,
            "distance": None,
            "within": None,
        }
    ]

    repository = RuleRepository()
    repository.add_rules(rules)
    matcher = ContentMatcher()

    def detection_event_generator(rule, event):
        return {"rule_text": rule["rule_text"]}

    evaluator = RuleEvaluationEngine(
        repository,
        matcher.matches,
        detection_event_generator,
    )
    event_fields = {
        "protocol": "TCP",
        "src_ip": "10.0.0.1",
        "src_port": 51000,
        "dst_ip": "10.0.0.2",
        "dst_port": 80,
    }

    match_events = [
        {**event_fields, "payload": "xxxxALERT!!"},
        {**event_fields, "payload": "TOKEN!"},
    ]
    no_match_events = [
        {**event_fields, "payload": "xxxxxxALERT"},
        {**event_fields, "payload": "xxxxxTOKEN"},
        event_fields,
    ]
    matches = [evaluator.evaluate(event) for event in match_events]
    no_matches = [evaluator.evaluate(event) for event in no_match_events]

    assert [result[0]["rule_text"] for result in matches] == [
        rules[0]["rule_text"],
        rules[1]["rule_text"],
    ]
    assert no_matches == [[], [], []]
    assert matches[0][0]["match_info"][0]["offset"] == 4
    assert matches[0][0]["match_info"][0]["depth"] == 6
    assert matches[1][0]["match_info"][0]["depth"] == 5

    invalid_rules = [
        'alert tcp any any -> any any (offset:1; sid:1;)',
        'alert tcp any any -> any any (content:"X"; offset:-1; sid:2;)',
        'alert tcp any any -> any any (content:"X"; depth:0; sid:3;)',
        'alert tcp any any -> any any (content:""; sid:4;)',
    ]
    invalid_results = [parser.parse(rule) for rule in invalid_rules]
    assert all(result["status"] == "invalid" for result in invalid_results)
    assert matcher.matches(
        {"content_conditions": [{"pattern": "X"}]},
        event_fields,
    ) == {"matched": False, "match_info": []}
    assert matcher.matches(
        {
            "content_conditions": [
                {
                    "pattern": "X",
                    "nocase": False,
                    "offset": 2,
                    "depth": 1,
                }
            ]
        },
        {"payload": "éX"},
    )["matched"]

    output_path.write_text(
        json.dumps(
            {
                "match_events": matches,
                "no_match_events": no_matches,
                "invalid_rule_statuses": [
                    {
                        "status": result["status"],
                        "reason": result["reason"],
                    }
                    for result in invalid_results
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
