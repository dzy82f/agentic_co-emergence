from agentic_co_emergence.models.models import GovernanceEventType, Issue, RuntimeProjection, RuntimeState

class StateProjection:
    def __init__(self, policy): self.policy = policy
    def from_events(self, session_id, events):
        p = RuntimeProjection(session_id=session_id)
        p.minimum_rounds = int(self.policy.get("minimum_rounds", p.minimum_rounds))
        p.handoff_required = bool(self.policy.get("handoff_required", p.handoff_required))
        p.facilitator_silent = bool(self.policy.get("facilitator_silent", p.facilitator_silent))
        p.active_agents = list(self.policy.get("active_agents", p.active_agents))
        for event in events:
            self.apply(p, event); p.governance_event_count += 1
        return p
    def apply(self, p, event):
        et, d = event.event_type, event.payload
        if et == GovernanceEventType.ISSUE_CAPTURED:
            p.issue = Issue(d.get("raw_user_question",""), d.get("working_title","Untitled Tychevia Issue"), d.get("framed_question",d.get("raw_user_question","")), d.get("domain","unspecified"), d.get("constraints",[]), "captured")
        elif et == GovernanceEventType.ISSUE_FRAMED:
            p.issue.framed_question=d.get("framed_question", p.issue.raw_user_question); p.issue.working_title=d.get("working_title", p.issue.working_title); p.issue.domain=d.get("domain", p.issue.domain); p.issue.status="framed"
        elif et == GovernanceEventType.STATE_CHANGED: p.state = RuntimeState(d["to_state"])
        elif et == GovernanceEventType.DISCUSSION_STARTED: p.current_speaker = d.get("initial_speaker")
        elif et == GovernanceEventType.ROUND_STARTED: p.current_round=d["round_number"]; p.turns_in_current_round=0
        elif et == GovernanceEventType.AGENT_TURN_ACCEPTED: p.total_turns += 1; p.turns_in_current_round += 1; p.previous_speaker=d.get("speaker")
        elif et == GovernanceEventType.SPEAKER_CHANGED: p.previous_speaker=d.get("from_speaker"); p.current_speaker=d.get("to_speaker")
        elif et == GovernanceEventType.ROUND_COMPLETED: p.completed_rounds=d["round_number"]
        elif et == GovernanceEventType.SYNTHESIS_UNLOCKED: p.synthesis_allowed=True
        elif et == GovernanceEventType.REVIEW_UNLOCKED: p.review_allowed=True
        elif et == GovernanceEventType.MODEL_OUTPUT_REJECTED: p.violations.append(d)
        elif et == GovernanceEventType.SESSION_ARCHIVED: p.state=RuntimeState.ARCHIVE
