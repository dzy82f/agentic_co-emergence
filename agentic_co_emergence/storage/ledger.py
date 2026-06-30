import json
from pathlib import Path

from agentic_co_emergence.models.event import LedgerEvent


class FileLedger:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, event_type: str, payload: dict) -> None:
        event = LedgerEvent(event_type=event_type, payload=payload)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(event.model_dump_json() + "\n")

    def read_all(self) -> list[LedgerEvent]:
        if not self.path.exists():
            return []
        events = []
        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                events.append(LedgerEvent.model_validate(json.loads(line)))
        return events
