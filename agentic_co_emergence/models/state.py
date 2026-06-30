from enum import StrEnum


class InquiryState(StrEnum):
    DRAFT = "DRAFT"
    OPEN = "OPEN"
    EXPLORING = "EXPLORING"
    CHALLENGING = "CHALLENGING"
    SYNTHESISING = "SYNTHESISING"
    REVIEWING = "REVIEWING"
    CLOSED = "CLOSED"
