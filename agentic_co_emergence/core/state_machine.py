from agentic_reasoning.models.state import InquiryState


ALLOWED_TRANSITIONS: dict[InquiryState, set[InquiryState]] = {
    InquiryState.DRAFT: {InquiryState.OPEN},
    InquiryState.OPEN: {InquiryState.EXPLORING},
    InquiryState.EXPLORING: {InquiryState.CHALLENGING},
    InquiryState.CHALLENGING: {InquiryState.SYNTHESISING},
    InquiryState.SYNTHESISING: {InquiryState.REVIEWING},
    InquiryState.REVIEWING: {InquiryState.CLOSED, InquiryState.EXPLORING},
    InquiryState.CLOSED: set(),
}


class InvalidTransitionError(ValueError):
    pass


def validate_transition(current: InquiryState, target: InquiryState) -> None:
    if target not in ALLOWED_TRANSITIONS[current]:
        raise InvalidTransitionError(f"Invalid transition: {current} -> {target}")
