from agentic_co_emergence.core.adsn_validator import ADSNValidator
from agentic_co_emergence.core.policy_loader import PolicyLoader
from agentic_co_emergence.models.models import RuntimeState, ValidationResult
class Validator:
    def __init__(self, policy=None):
        self.policy = policy or PolicyLoader().load()
        self.adsn_validator = ADSNValidator(self.policy)

    def validate(self, proposed, projection):
        if proposed.attempted_synthesis and not projection.synthesis_allowed: return ValidationResult(False, "Synthesis attempted before permitted.")
        if proposed.attempted_review and not projection.review_allowed: return ValidationResult(False, "Review attempted before permitted.")
        if projection.state == RuntimeState.DISCUSSION:
            if proposed.speaker != projection.current_speaker: return ValidationResult(False, f"Expected speaker {projection.current_speaker}.")
            if projection.handoff_required:
                ok, reason = self.adsn_validator.validate_handoff(
                    projection.current_speaker,
                    proposed.handoff_to,
                    projection.active_agents,
                    projection.previous_speaker,
                )
                if not ok:
                    return ValidationResult(False, reason)
        return ValidationResult(True, "")
