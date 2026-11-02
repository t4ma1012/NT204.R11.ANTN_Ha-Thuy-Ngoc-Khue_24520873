from typing import Callable, Dict, List

from src.engine.repository import RuleRepository


class RuleEvaluationEngine:
    def __init__(
        self,
        repository: RuleRepository,
        content_matcher: Callable[[Dict[str, object], Dict[str, object]], bool],
        detection_event_generator: Callable[
            [Dict[str, object], Dict[str, object]],
            Dict[str, object],
        ],
    ) -> None:
        self._repository = repository
        self._content_matcher = content_matcher
        self._detection_event_generator = detection_event_generator

    def evaluate(self, event: Dict[str, object]) -> List[Dict[str, object]]:
        detection_events = []

        for rule in self._repository.get_candidates(event):
            if self._content_matcher(rule, event):
                detection_events.append(
                    self._detection_event_generator(rule, event)
                )

        return detection_events
