import re
from agentic_co_emergence.models.models import ProposedModelEvent
class EventParser:
    def parse_model_output(self, text, projection):
        content=text.strip()
        speaker=projection.current_speaker if projection.current_speaker and content.startswith(f"{projection.current_speaker}:") else None
        m=re.search(r"^HANDOFF:\s*(.+?)\s*$", text, re.MULTILINE)
        lower=content.lower()
        return ProposedModelEvent(speaker, content, m.group(1).strip() if m else None, lower.startswith("synthesis:") or "in conclusion" in lower, lower.startswith("review:") or "review protocol" in lower, text)
