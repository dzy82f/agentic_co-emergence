from pathlib import Path


class ProtocolLoader:
    def __init__(self, policy, protocol_dir: str | Path | None = None):
        self.policy = policy
        self.protocol_dir = Path(protocol_dir) if protocol_dir is not None else Path(__file__).resolve().parents[1] / "protocols"

    def load_for_state(self, projection):
        protocols = {}
        for name in self.policy.get("state_protocols", {}).get(projection.state.value, []):
            path = self.protocol_dir / f"{name}.md"
            protocols[name] = path.read_text(encoding="utf-8") if path.exists() else f"[{name}] Placeholder protocol content."
        return protocols
