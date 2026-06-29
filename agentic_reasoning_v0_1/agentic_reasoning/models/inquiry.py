from pydantic import BaseModel, Field


class InquiryEnvelope(BaseModel):
    id: str
    title: str
    question: str
    domain: str
    constraints: list[str] = Field(default_factory=list)
    required_perspectives: list[str] = Field(default_factory=list)
    success_criteria: list[str] = Field(default_factory=list)
    minimum_explorations: int = 2
    minimum_challenges: int = 1


class Contribution(BaseModel):
    agent: str
    stage: str
    content: str
