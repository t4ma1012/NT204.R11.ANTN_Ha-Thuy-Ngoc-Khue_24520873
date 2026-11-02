from typing import Dict, List, Optional


class FlowMatcher:
    def matches(
        self,
        conditions: List[str],
        flow_context: Optional[Dict[str, object]],
    ) -> bool:
        if not conditions:
            return True

        if not isinstance(flow_context, dict):
            return False

        for condition in conditions:
            if condition == "to_server":
                if flow_context.get("direction") != "to_server":
                    return False
            elif condition == "to_client":
                if flow_context.get("direction") != "to_client":
                    return False
            elif condition == "established":
                if flow_context.get("tcp_state") != "ESTABLISHED":
                    return False
            elif condition == "not_established":
                if flow_context.get("tcp_state") not in {"NEW", "HANDSHAKE"}:
                    return False
            else:
                return False

        return True
