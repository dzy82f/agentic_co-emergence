class ADSNValidator:
    """
    Lightweight ADSN guard.

    This does not choose the next speaker. It validates the proposed handoff
    against simple constitutional and social-network rules.
    """

    def __init__(self, policy):
        self.policy = policy
        self.adsn_policy = policy.get("adsn", {})

    def validate_handoff(self, current_speaker, proposed_handoff, active_agents, previous_speaker=None):
        if not proposed_handoff:
            return False, "Required HANDOFF target missing."

        if proposed_handoff not in active_agents:
            return False, f"Invalid handoff target: {proposed_handoff}"

        if not self.adsn_policy.get("allow_self_handoff", False):
            if proposed_handoff == current_speaker:
                return False, "Self-handoff is not allowed."

        if self.adsn_policy.get("avoid_repeating_previous_speaker", True):
            if previous_speaker and proposed_handoff == previous_speaker and len(active_agents) > 2:
                return False, "Handoff returns immediately to previous speaker without need."

        return True, ""
