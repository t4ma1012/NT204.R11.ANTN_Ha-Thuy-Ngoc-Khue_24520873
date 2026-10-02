import json
from pathlib import Path

from src.flow.tracker import FlowTracker


def write_output(path, data):
    output_file = Path(path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    output_file.write_text(
        json.dumps(data, indent=2),
        encoding="utf-8",
    )


def test_tcp_handshake():
    tracker = FlowTracker()

    events = [
        {
            "timestamp": 1,
            "protocol": "TCP",
            "src_ip": "10.0.0.1",
            "dst_ip": "10.0.0.2",
            "src_port": 12345,
            "dst_port": 80,
            "flags": "S",
            "payload_length": 0,
        },
        {
            "timestamp": 2,
            "protocol": "TCP",
            "src_ip": "10.0.0.2",
            "dst_ip": "10.0.0.1",
            "src_port": 80,
            "dst_port": 12345,
            "flags": "SA",
            "payload_length": 0,
        },
        {
            "timestamp": 3,
            "protocol": "TCP",
            "src_ip": "10.0.0.1",
            "dst_ip": "10.0.0.2",
            "src_port": 12345,
            "dst_port": 80,
            "flags": "A",
            "payload_length": 0,
        },
    ]

    flows = []

    for event in events:
        flows.append(tracker.process(event))

    flow = flows[-1]

    assert len(tracker.get_active_flows()) == 1
    assert flow.syn_count == 2
    assert flow.ack_count == 2
    assert flow.tcp_state == "ESTABLISHED"

    write_output(
        "TEST/flow/tcp_handshake/output.json",
        flow.to_dict(),
    )