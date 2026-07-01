from agentic_co_emergence.models.models import GovernanceEvent, GovernanceEventType, RuntimeState
class TransitionEngine:
    def __init__(self, policy): self.policy=policy
    def events_for_user_input(self,p,user_input):
        ev=[]
        if p.state==RuntimeState.IDLE:
            ev.append(GovernanceEvent(p.session_id, GovernanceEventType.SESSION_STARTED, {}))
            ev.append(GovernanceEvent(p.session_id, GovernanceEventType.STATE_CHANGED, {"from_state":"IDLE","to_state":"STARTUP"}))
        if user_input and not p.issue.raw_user_question:
            ev.append(GovernanceEvent(p.session_id, GovernanceEventType.ISSUE_CAPTURED, {"raw_user_question":user_input,"working_title":"Untitled Tychevia Issue","framed_question":user_input,"domain":"unspecified","constraints":[]}))
        return ev
    def events_for_accepted_output(self,p,proposed):
        ev=[GovernanceEvent(p.session_id, GovernanceEventType.MODEL_OUTPUT_ACCEPTED, {"content":proposed.content,"state":p.state.value})]
        if p.state==RuntimeState.ISSUE_FRAMING:
            ev.append(GovernanceEvent(p.session_id, GovernanceEventType.ISSUE_FRAMED, {"working_title":p.issue.working_title or "Untitled Tychevia Issue","framed_question":p.issue.raw_user_question,"domain":p.issue.domain or "unspecified"}))
        if p.state==RuntimeState.DISCUSSION:
            ev.append(GovernanceEvent(p.session_id, GovernanceEventType.AGENT_TURN_ACCEPTED, {"speaker":proposed.speaker,"content":proposed.content,"handoff_to":proposed.handoff_to,"round_number":p.current_round,"turns_in_current_round_before":p.turns_in_current_round}))
            ev.append(GovernanceEvent(p.session_id, GovernanceEventType.SPEAKER_CHANGED, {"from_speaker":proposed.speaker,"to_speaker":proposed.handoff_to}))
            if (p.turns_in_current_round+1)>=len(p.active_agents): ev.append(GovernanceEvent(p.session_id, GovernanceEventType.ROUND_COMPLETED, {"round_number":p.current_round}))
        nxt=self._next_state(p)
        if nxt and nxt!=p.state.value:
            ev.append(GovernanceEvent(p.session_id, GovernanceEventType.STATE_CHANGED, {"from_state":p.state.value,"to_state":nxt}))
            if nxt==RuntimeState.DISCUSSION.value and p.state==RuntimeState.ISSUE_FRAMING:
                initial=self.policy.get("initial_speaker","Tenzing")
                ev.append(GovernanceEvent(p.session_id, GovernanceEventType.DISCUSSION_STARTED, {"initial_speaker":initial}))
                ev.append(GovernanceEvent(p.session_id, GovernanceEventType.ROUND_STARTED, {"round_number":1}))
            elif nxt==RuntimeState.DISCUSSION.value and p.state==RuntimeState.ROUND_CHECK:
                ev.append(GovernanceEvent(p.session_id, GovernanceEventType.ROUND_STARTED, {"round_number":p.completed_rounds+1}))
            if nxt==RuntimeState.SYNTHESIS.value: ev.append(GovernanceEvent(p.session_id, GovernanceEventType.SYNTHESIS_UNLOCKED, {}))
            if nxt==RuntimeState.REVIEW.value: ev.append(GovernanceEvent(p.session_id, GovernanceEventType.REVIEW_UNLOCKED, {}))
            if nxt==RuntimeState.ARCHIVE.value: ev.append(GovernanceEvent(p.session_id, GovernanceEventType.SESSION_ARCHIVED, {}))
        return ev
    def event_for_rejected_output(self,p,proposed,reason): return GovernanceEvent(p.session_id, GovernanceEventType.MODEL_OUTPUT_REJECTED, {"reason":reason,"content":proposed.content,"state":p.state.value})
    def _next_state(self,p):
        rule=self.policy.get("transitions",{}).get(p.state.value,{}).get("on_accepted_output")
        if rule is None: return None
        if isinstance(rule,str): return rule
        for item in rule:
            guard=item.get("if")
            if guard is None or (guard=="round_complete_after_turn" and (p.turns_in_current_round+1)>=len(p.active_agents)) or (guard=="minimum_rounds_complete" and p.completed_rounds>=p.minimum_rounds):
                return item["next"]
