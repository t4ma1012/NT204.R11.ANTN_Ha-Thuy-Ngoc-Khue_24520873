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

def test_bidirectional_same_flow():
    tracker = FlowTracker()

    event_a = {
        "timestamp": 1,
        "protocol": "TCP",
        "src_ip": "10.0.0.1",
        "dst_ip": "10.0.0.2",
        "src_port": 5000,
        "dst_port": 80,
        "flags": "A",
        "payload_length": 100,
    }

    event_b = {
        "timestamp": 2,
        "protocol": "TCP",
        "src_ip": "10.0.0.2",
        "dst_ip": "10.0.0.1",
        "src_port": 80,
        "dst_port": 5000,
        "flags": "A",
        "payload_length": 200,
    }

    flow_a = tracker.process(event_a)
    flow_b = tracker.process(event_b)

    assert flow_a.flow_id == flow_b.flow_id
    assert flow_b.packet_count == 2
    assert flow_b.forward_packets == 1
    assert flow_b.backward_packets == 1

    write_output(
        "TEST/flow/bidirectional/output.json",
        flow_b.to_dict(),
    )


def test_tcp_close():
    tracker = FlowTracker()

    events = [
        {
            "timestamp": 1,
            "protocol": "TCP",
            "src_ip": "10.0.0.1",
            "dst_ip": "10.0.0.2",
            "src_port": 5000,
            "dst_port": 80,
            "flags": "F",
            "payload_length": 0,
        },
        {
            "timestamp": 2,
            "protocol": "TCP",
            "src_ip": "10.0.0.2",
            "dst_ip": "10.0.0.1",
            "src_port": 80,
            "dst_port": 5000,
            "flags": "F",
            "payload_length": 0,
        },
    ]

    flow = None

    for event in events:
        flow = tracker.process(event)

    assert flow.tcp_state == "CLOSED"
    assert flow.fin_count == 2

    write_output(
        "TEST/flow/tcp_close/output.json",
        flow.to_dict(),
    )

def test_udp_flow():
    tracker = FlowTracker()

    query = {
        "timestamp": 1,
        "protocol": "UDP",
        "src_ip": "10.0.0.1",
        "dst_ip": "8.8.8.8",
        "src_port": 50000,
        "dst_port": 53,
        "payload_length": 32,
    }

    response = {
        "timestamp": 2,
        "protocol": "UDP",
        "src_ip": "8.8.8.8",
        "dst_ip": "10.0.0.1",
        "src_port": 53,
        "dst_port": 50000,
        "payload_length": 64,
    }

    flow = tracker.process(query)
    flow = tracker.process(response)

    assert flow.protocol == "UDP"
    assert flow.packet_count == 2
    assert flow.byte_count == 96
    assert flow.forward_packets == 1
    assert flow.backward_packets == 1

    write_output(
        "TEST/flow/udp/output.json",
        flow.to_dict(),
    )

def test_concurrent_flows():
    tracker = FlowTracker()

    events = [
        {
            "timestamp": 1,
            "protocol": "TCP",
            "src_ip": "10.0.0.1",
            "dst_ip": "10.0.0.2",
            "src_port": 5000,
            "dst_port": 80,
            "flags": "S",
            "payload_length": 0,
        },
        {
            "timestamp": 2,
            "protocol": "TCP",
            "src_ip": "10.0.0.1",
            "dst_ip": "10.0.0.2",
            "src_port": 5001,
            "dst_port": 80,
            "flags": "S",
            "payload_length": 0,
        },
    ]

    flows = [
        tracker.process(event)
        for event in events
    ]

    assert len(tracker.get_active_flows()) == 2
    assert flows[0].flow_id != flows[1].flow_id

    write_output(
        "TEST/flow/concurrent/output.json",
        [
            flow.to_dict()
            for flow in flows
        ],
    )

def test_idle_timeout():
    tracker = FlowTracker(idle_timeout=10)

    event = {
        "timestamp": 1,
        "protocol": "UDP",
        "src_ip": "10.0.0.1",
        "dst_ip": "8.8.8.8",
        "src_port": 50000,
        "dst_port": 53,
        "payload_length": 20,
    }

    tracker.process(event)

    assert len(tracker.get_active_flows()) == 1

    expired = tracker.expire(12)

    assert len(expired) == 1
    assert len(tracker.get_active_flows()) == 0

    write_output(
        "TEST/flow/timeout/output.json",
        {
            "expired": [
                flow.to_dict()
                for flow in expired
            ],
            "active_flows": [],
        },
    )
def test_flow_statistics():
    tracker = FlowTracker()

    events = [
        {
            "timestamp": 1,
            "protocol": "TCP",
            "src_ip": "10.0.0.1",
            "dst_ip": "10.0.0.2",
            "src_port": 5000,
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
            "dst_port": 5000,
            "flags": "SA",
            "payload_length": 0,
        },
        {
            "timestamp": 3,
            "protocol": "TCP",
            "src_ip": "10.0.0.1",
            "dst_ip": "10.0.0.2",
            "src_port": 5000,
            "dst_port": 80,
            "flags": "A",
            "payload_length": 100,
        },
        {
            "timestamp": 4,
            "protocol": "TCP",
            "src_ip": "10.0.0.2",
            "dst_ip": "10.0.0.1",
            "src_port": 80,
            "dst_port": 5000,
            "flags": "A",
            "payload_length": 200,
        },
    ]

    flow = None

    for event in events:
        flow = tracker.process(event)

    assert flow.packet_count == 4
    assert flow.byte_count == 300

    assert flow.forward_packets == 2
    assert flow.backward_packets == 2

    assert flow.forward_bytes == 100
    assert flow.backward_bytes == 200

    assert flow.syn_count == 2
    assert flow.ack_count == 2

    assert flow.duration() == 3

    assert len(tracker.get_active_flows()) == 1

    write_output(
        "TEST/flow/statistics/output.json",
        flow.to_dict(),
    )
    