from pathlib import Path


class PersonaManager:
    def __init__(self, persona_dir: str | Path | None = None):
        self.persona_dir = Path(persona_dir) if persona_dir is not None else Path(__file__).resolve().parent

    def load(self, agent_name: str | None) -> str:
        if not agent_name:
            return ""
        path = self.persona_dir / f"{agent_name}.md"
        if not path.exists():
            return f"# {agent_name}\n\nNo persona file found."
        return path.read_text(encoding="utf-8")
