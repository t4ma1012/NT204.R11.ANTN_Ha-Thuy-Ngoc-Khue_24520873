from typing import Callable, Dict, List, Optional

from src.engine.flow_matcher import FlowMatcher
from src.engine.packet_matcher import PacketMatcher
from src.engine.repository import RuleRepository


class RuleEvaluationEngine:
    def __init__(
        self,
        repository: RuleRepository,
        content_matcher: Callable[[Dict[str, object], Dict[str, object]], object],
        detection_event_generator: Callable[
            [Dict[str, object], Dict[str, object]],
            Dict[str, object],
        ],
    ) -> None:
        self._repository = repository
        self._content_matcher = content_matcher
        self._detection_event_generator = detection_event_generator
        self._flow_matcher = FlowMatcher()
        self._packet_matcher = PacketMatcher()

    def evaluate(
        self,
        event: Dict[str, object],
        flow_context: Optional[Dict[str, object]] = None,
    ) -> List[Dict[str, object]]:
        detection_events = []

        for rule in self._repository.get_candidates(event):
            flow_conditions = rule.get("flow_conditions")
            if flow_conditions and not self._flow_matcher.matches(
                flow_conditions,
                flow_context,
            ):
                continue
            if not self._packet_matcher.matches(rule, event):
                continue

            content_result = self._content_matcher(rule, event)
            if isinstance(content_result, dict):
                matched = bool(content_result.get("matched"))
                match_info = content_result.get("match_info", [])
            else:
                matched = bool(content_result)
                match_info = []

            if matched:
                detection_event = self._detection_event_generator(rule, event)
                if match_info:
                    detection_event["match_info"] = match_info
                detection_events.append(detection_event)

        return detection_events
