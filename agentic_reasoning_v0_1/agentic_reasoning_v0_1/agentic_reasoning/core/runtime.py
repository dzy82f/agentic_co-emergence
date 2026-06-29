from pathlib import Path

from agentic_reasoning.core.state_machine import validate_transition
from agentic_reasoning.models.inquiry import Contribution, InquiryEnvelope
from agentic_reasoning.models.state import InquiryState
from agentic_reasoning.storage.ledger import FileLedger


class GovernanceError(ValueError):
    pass


class AgenticReasoningRuntime:
    def __init__(self, envelope: InquiryEnvelope, ledger_path: Path | None = None):
        self.envelope = envelope
        self.state = InquiryState.DRAFT
        self.contributions: list[Contribution] = []
        self.ledger = FileLedger(ledger_path or Path(".ledger") / f"{envelope.id}.jsonl")
        self.ledger.append("inquiry_created", envelope.model_dump())

    def transition_to(self, target: InquiryState) -> None:
        self._check_governance(target)
        validate_transition(self.state, target)
        previous = self.state
        self.state = target
        self.ledger.append("state_transition", {"from": previous, "to": target})

    def contribute(self, contribution: Contribution) -> None:
        if contribution.stage != self.state:
            raise GovernanceError(
                f"Contribution stage {contribution.stage} does not match current state {self.state}"
            )
        self.contributions.append(contribution)
        self.ledger.append("contribution", contribution.model_dump())

    def _check_governance(self, target: InquiryState) -> None:
        if target == InquiryState.SYNTHESISING:
            explorations = [c for c in self.contributions if c.stage == InquiryState.EXPLORING]
            challenges = [c for c in self.contributions if c.stage == InquiryState.CHALLENGING]
            if len(explorations) < self.envelope.minimum_explorations:
                raise GovernanceError("Cannot synthesise before minimum exploration contributions are met")
            if len(challenges) < self.envelope.minimum_challenges:
                raise GovernanceError("Cannot synthesise before minimum challenge contributions are met")
