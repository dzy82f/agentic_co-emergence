from agentic_co_emergence.models.models import ReasoningEventType, ReasoningProjection

class ReasoningProjector:
    def from_events(self, session_id, events):
        p = ReasoningProjection(session_id=session_id)
        for e in events:
            item = {"event_id": e.event_id, "speaker": e.speaker, "content": e.content, "source_governance_event_id": e.source_governance_event_id, **e.payload}
            if e.event_type == ReasoningEventType.CLAIM_REGISTERED: p.claims.append(item)
            elif e.event_type == ReasoningEventType.QUESTION_REGISTERED: p.questions.append(item)
            elif e.event_type == ReasoningEventType.ASSUMPTION_REGISTERED: p.assumptions.append(item)
            elif e.event_type == ReasoningEventType.CHALLENGE_REGISTERED: p.challenges.append(item)
            elif e.event_type == ReasoningEventType.AGREEMENT_REGISTERED: p.agreements.append(item)
            elif e.event_type == ReasoningEventType.UNCERTAINTY_REGISTERED: p.uncertainties.append(item)
            elif e.event_type == ReasoningEventType.HANDOFF_RATIONALE_REGISTERED: p.handoff_rationales.append(item)
        return p
