from typing import Dict, List, Optional


class DetectionEventGenerator:
    def generate(
        self,
        rule: Dict[str, object],
        event: Dict[str, object],
        flow_context: Optional[Dict[str, object]] = None,
        match_info: Optional[List[Dict[str, object]]] = None,
    ) -> Dict[str, object]:
        metadata = rule.get("metadata")
        if not isinstance(metadata, dict):
            metadata = {}

        if not isinstance(flow_context, dict):
            flow_context = {}
        flow_id = flow_context.get("flow_id")
        if flow_id is None:
            flow_id = event.get("flow_id")
        event_match_info = list(match_info or [])
        self._append_packet_match_info(
            rule,
            event,
            flow_context,
            event_match_info,
        )
        if not event_match_info:
            event_match_info.append(
                {
                    "type": "header",
                    "rule_header": rule.get("header"),
                }
            )

        detection_event = {
            "timestamp": event.get("timestamp"),
            "sid": metadata.get("sid"),
            "rev": metadata.get("rev"),
            "msg": metadata.get("msg"),
            "src_ip": event.get("src_ip"),
            "src_port": event.get("src_port"),
            "dst_ip": event.get("dst_ip"),
            "dst_port": event.get("dst_port"),
            "protocol": event.get("protocol"),
            "application_protocol": event.get("application_protocol"),
            "flow_id": flow_id,
            "match_info": event_match_info,
        }

        for optional_field in ("priority", "classtype"):
            if optional_field in metadata:
                detection_event[optional_field] = metadata[optional_field]

        return detection_event

    @staticmethod
    def _append_packet_match_info(
        rule: Dict[str, object],
        event: Dict[str, object],
        flow_context: Dict[str, object],
        match_info: List[Dict[str, object]],
    ) -> None:
        flags_condition = rule.get("flags_condition")
        if flags_condition is not None:
            match_info.append(
                {
                    "keyword": "flags",
                    "condition": flags_condition,
                    "matched_value": event.get("flags"),
                }
            )

        dsize_condition = rule.get("dsize_condition")
        if dsize_condition is not None:
            match_info.append(
                {
                    "keyword": "dsize",
                    "condition": dsize_condition,
                    "matched_value": event.get("payload_length"),
                }
            )

        flow_conditions = rule.get("flow_conditions")
        if flow_conditions:
            match_info.append(
                {
                    "keyword": "flow",
                    "conditions": flow_conditions,
                    "matched_context": {
                        "direction": flow_context.get("direction"),
                        "tcp_state": flow_context.get("tcp_state"),
                    },
                }
            )
