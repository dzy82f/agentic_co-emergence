import pytest

from agentic_reasoning.core.state_machine import InvalidTransitionError, validate_transition
from agentic_reasoning.models.state import InquiryState


def test_valid_transition():
    validate_transition(InquiryState.DRAFT, InquiryState.OPEN)


def test_invalid_transition():
    with pytest.raises(InvalidTransitionError):
        validate_transition(InquiryState.DRAFT, InquiryState.SYNTHESISING)
