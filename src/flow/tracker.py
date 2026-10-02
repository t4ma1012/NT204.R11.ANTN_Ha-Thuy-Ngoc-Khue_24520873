from .flow import Flow


class FlowTracker:
    def __init__(self, idle_timeout=60):
        self.idle_timeout = idle_timeout
        self.active_flows = {}

    def _endpoint(self, event):
        return (
            event["src_ip"],
            int(event["src_port"]),
        )

    def _canonical_key(self, event):
        endpoint_a = self._endpoint(event)

        endpoint_b = (
            event["dst_ip"],
            int(event["dst_port"]),
        )

        endpoints = sorted(
            [endpoint_a, endpoint_b]
        )

        return (
            event["protocol"],
            endpoints[0],
            endpoints[1],
        )

    def _flow_id(self, key):
        protocol, endpoint_a, endpoint_b = key

        return (
            f"{protocol}-"
            f"{endpoint_a[0]}:{endpoint_a[1]}-"
            f"{endpoint_b[0]}:{endpoint_b[1]}"
        )

    def _direction(self, flow, event):
        endpoint = self._endpoint(event)

        if endpoint == flow.endpoint_a:
            return "forward"

        return "backward"

    def _update_tcp_state(self, flow, flags):
        flags = set(flags)

        if "R" in flags:
            flow.rst_count += 1
            flow.tcp_state = "RESET"
            return

        if "S" in flags:
            flow.syn_count += 1

            if "A" in flags:
                flow.ack_count += 1
                flow.tcp_state = "HANDSHAKE"
            else:
                flow.tcp_state = "HANDSHAKE"

            return
        if "F" in flags:
            flow.fin_count += 1
            flow.tcp_state = "CLOSING"
            return

        if flow.tcp_state == "HANDSHAKE" and "A" in flags:
            flow.ack_count += 1
            flow.tcp_state = "ESTABLISHED"

    def process(self, event):
        self.expire(event["timestamp"])

        key = self._canonical_key(event)

        if key not in self.active_flows:
            endpoint_a = key[1]
            endpoint_b = key[2]

            flow = Flow(
                flow_id=self._flow_id(key),
                protocol=event["protocol"],
                endpoint_a=endpoint_a,
                endpoint_b=endpoint_b,
                start_time=event["timestamp"],
            )

            self.active_flows[key] = flow

        flow = self.active_flows[key]

        direction = self._direction(flow, event)

        byte_count = int(
            event.get("payload_length", 0)
        )

        flow.packet_count += 1
        flow.byte_count += byte_count
        flow.last_seen = event["timestamp"]

        if direction == "forward":
            flow.forward_packets += 1
            flow.forward_bytes += byte_count
        else:
            flow.backward_packets += 1
            flow.backward_bytes += byte_count

        if event["protocol"] == "TCP":
            self._update_tcp_state(
                flow,
                event.get("flags", ""),
            )

            flags = set(event.get("flags", ""))

            if "F" in flags and flow.fin_count >= 2:
                flow.tcp_state = "CLOSED"

        return flow

    def expire(self, current_time):
        expired = []

        for key, flow in list(
            self.active_flows.items()
        ):
            if (
                current_time - flow.last_seen
                >= self.idle_timeout
            ):
                expired.append(flow)
                del self.active_flows[key]

        return expired

    def get_active_flows(self):
        return list(self.active_flows.values())