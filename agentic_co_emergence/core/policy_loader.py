import json
from pathlib import Path


class PolicyLoader:
    def __init__(self, policy_path: str | Path | None = None):
        self.policy_path = Path(policy_path) if policy_path is not None else Path(__file__).with_name("runtime_policy.json")

    def load(self):
        return json.loads(self.policy_path.read_text(encoding="utf-8"))
