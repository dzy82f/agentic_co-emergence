import json
from pathlib import Path
from typing import Iterable, Type, TypeVar
from agentic_co_emergence.models.models import GovernanceEvent, ReasoningEvent, KnowledgeEvent, MemoryEvent, SemanticEvent

T = TypeVar("T")

class JsonlEventStore:
    def __init__(self, event_cls: Type[T], file_id: str, storage_dir: str | Path):
        self.event_cls = event_cls
        self.file_id = file_id
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.path = self.storage_dir / f"{file_id}.jsonl"
    def append_many(self, events: Iterable[T]) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            for event in events:
                f.write(json.dumps(event.to_dict(), ensure_ascii=False) + "\n")
    def append(self, event: T) -> None:
        self.append_many([event])
    def load(self):
        if not self.path.exists():
            return []
        return [self.event_cls.from_dict(json.loads(line)) for line in self.path.read_text(encoding="utf-8").splitlines() if line.strip()]
    def reset(self):
        if self.path.exists():
            self.path.unlink()

class GovernanceEventStore(JsonlEventStore):
    def __init__(self, session_id: str, storage_dir: str | Path = "runtime_data/governance_events"):
        super().__init__(GovernanceEvent, session_id, storage_dir)

class ReasoningEventStore(JsonlEventStore):
    def __init__(self, session_id: str, storage_dir: str | Path = "runtime_data/reasoning_events"):
        super().__init__(ReasoningEvent, session_id, storage_dir)

class KnowledgeEventStore(JsonlEventStore):
    def __init__(self, session_id: str, storage_dir: str | Path = "runtime_data/knowledge_events"):
        super().__init__(KnowledgeEvent, session_id, storage_dir)

class MemoryEventStore(JsonlEventStore):
    def __init__(self, memory_space_id: str, storage_dir: str | Path = "runtime_data/memory_events"):
        super().__init__(MemoryEvent, memory_space_id, storage_dir)

class SemanticEventStore(JsonlEventStore):
    def __init__(self, memory_space_id: str, storage_dir: str | Path = "runtime_data/semantic_events"):
        super().__init__(SemanticEvent, memory_space_id, storage_dir)
