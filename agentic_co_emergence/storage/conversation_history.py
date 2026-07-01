class ConversationHistory:
    def __init__(self, governance_store):
        self.governance_store = governance_store

    def recent_turns(self, limit: int = 12) -> str:
        turns = []
        for event in self.governance_store.load():
            if getattr(event, "event_type", None).value == "AGENT_TURN_ACCEPTED":
                content = event.payload.get("content", "")
                if content.strip():
                    turns.append(content)
        return "\n\n---\n\n".join(turns[-limit:]) if turns else "[No prior discussion turns.]"
