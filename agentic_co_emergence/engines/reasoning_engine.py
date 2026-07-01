import re
from agentic_co_emergence.models.models import GovernanceEventType, ReasoningEvent, ReasoningEventType

class ReasoningEngine:
    PATTERNS = [
        (ReasoningEventType.CLAIM_REGISTERED, r"^\s*(?:[A-Za-z]+:\s*)?CLAIM:\s*(.+)", "claim"),
        (ReasoningEventType.QUESTION_REGISTERED, r"^\s*(?:[A-Za-z]+:\s*)?QUESTION:\s*(.+)", "question"),
        (ReasoningEventType.ASSUMPTION_REGISTERED, r"^\s*(?:[A-Za-z]+:\s*)?ASSUMPTION:\s*(.+)", "assumption"),
        (ReasoningEventType.CHALLENGE_REGISTERED, r"^\s*(?:[A-Za-z]+:\s*)?CHALLENGE:\s*(.+)", "challenge"),
        (ReasoningEventType.AGREEMENT_REGISTERED, r"^\s*(?:[A-Za-z]+:\s*)?AGREEMENT:\s*(.+)", "agreement"),
        (ReasoningEventType.UNCERTAINTY_REGISTERED, r"^\s*(?:[A-Za-z]+:\s*)?UNCERTAINTY:\s*(.+)", "uncertainty"),
    ]

    def extract_from_governance_event(self, event):
        if event.event_type != GovernanceEventType.AGENT_TURN_ACCEPTED:
            return []
        speaker = event.payload.get("speaker")
        content = event.payload.get("content", "")
        body = self._strip_handoff(content)
        events = []
        for event_type, pattern, kind in self.PATTERNS:
            match = re.search(pattern, body, re.IGNORECASE | re.MULTILINE | re.DOTALL)
            if match:
                events.append(ReasoningEvent(event.session_id, event_type, speaker, self._clean(match.group(1)), event.event_id, {"kind": kind, "extraction": "labelled"}))
                break
        if not events:
            event_type, kind = self._fallback_kind(body)
            events.append(ReasoningEvent(event.session_id, event_type, speaker, self._first_sentence(body), event.event_id, {"kind": kind, "extraction": "fallback"}))
        handoff_to = event.payload.get("handoff_to")
        if handoff_to:
            events.append(ReasoningEvent(event.session_id, ReasoningEventType.HANDOFF_RATIONALE_REGISTERED, speaker, f"{speaker} handed off to {handoff_to}.", event.event_id, {"handoff_to": handoff_to}))
        return events

    def _fallback_kind(self, text):
        lower = text.lower()
        if "?" in text or "what would" in lower or "how might" in lower:
            return ReasoningEventType.QUESTION_REGISTERED, "question"
        if "challenge" in lower or "danger" in lower or "risk" in lower or "wary" in lower:
            return ReasoningEventType.CHALLENGE_REGISTERED, "challenge"
        if "assuming" in lower or "assumption" in lower:
            return ReasoningEventType.ASSUMPTION_REGISTERED, "assumption"
        if "uncertain" in lower or "uncertainty" in lower:
            return ReasoningEventType.UNCERTAINTY_REGISTERED, "uncertainty"
        if "i agree" in lower or "agreement" in lower:
            return ReasoningEventType.AGREEMENT_REGISTERED, "agreement"
        return ReasoningEventType.CLAIM_REGISTERED, "claim"

    def _strip_handoff(self, text):
        return re.split(r"\n\s*HANDOFF:", text, flags=re.IGNORECASE)[0].strip()

    def _clean(self, text):
        return " ".join(self._strip_handoff(text).split())

    def _first_sentence(self, text):
        text = re.sub(r"^[A-Za-z]+:\s*", "", self._strip_handoff(text)).strip()
        parts = re.split(r"(?<=[.!?])\s+", text)
        return self._clean(parts[0] if parts else text)
