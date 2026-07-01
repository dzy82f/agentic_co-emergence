import json
from pathlib import Path

class TelemetryStore:
    def __init__(self, session_id: str, storage_dir: str | Path = "runtime_data/telemetry"):
        self.path = Path(storage_dir) / f"{session_id}.jsonl"
        self.path.parent.mkdir(parents=True, exist_ok=True)
    def append_many(self, events):
        with self.path.open("a", encoding="utf-8") as f:
            for event in events:
                f.write(json.dumps(event.to_dict(), ensure_ascii=False) + "\n")
    def reset(self):
        if self.path.exists(): self.path.unlink()
