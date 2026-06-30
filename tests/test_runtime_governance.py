import pytest

from agentic_co_emergence.core.runtime import AgenticReasoningRuntime, GovernanceError
from agentic_co_emergence.models.inquiry import Contribution, InquiryEnvelope
from agentic_co_emergence.models.state import InquiryState


def envelope() -> InquiryEnvelope:
    return InquiryEnvelope(
        id="test",
        title="Test",
        question="What is being tested?",
        domain="Runtime governance",
        minimum_explorations=2,
        minimum_challenges=1,
    )


def test_synthesis_blocked_until_requirements_met(tmp_path):
    runtime = AgenticReasoningRuntime(envelope(), tmp_path / "ledger.jsonl")
    runtime.transition_to(InquiryState.OPEN)
    runtime.transition_to(InquiryState.EXPLORING)
    runtime.contribute(Contribution(agent="A", stage="EXPLORING", content="One exploration"))
    runtime.transition_to(InquiryState.CHALLENGING)
    runtime.contribute(Contribution(agent="B", stage="CHALLENGING", content="One challenge"))

    with pytest.raises(GovernanceError):
        runtime.transition_to(InquiryState.SYNTHESISING)
