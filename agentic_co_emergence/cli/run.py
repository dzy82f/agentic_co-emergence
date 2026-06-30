import sys
from pathlib import Path

import yaml

from agentic_co_emergence.core.runtime import AgenticReasoningRuntime
from agentic_co_emergence.models.inquiry import Contribution, InquiryEnvelope
from agentic_co_emergence.models.state import InquiryState


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python -m agentic_co_emergence.cli.run <inquiry.yaml>")
        return 2

    path = Path(sys.argv[1])
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    envelope = InquiryEnvelope.model_validate(data)
    runtime = AgenticReasoningRuntime(envelope)

    runtime.transition_to(InquiryState.OPEN)
    runtime.transition_to(InquiryState.EXPLORING)
    runtime.contribute(Contribution(agent="Aletheia", stage="EXPLORING", content="Clarify terms and assumptions."))
    runtime.contribute(Contribution(agent="Joan", stage="EXPLORING", content="Identify governance boundaries and accountabilities."))
    runtime.transition_to(InquiryState.CHALLENGING)
    runtime.contribute(Contribution(agent="Harry", stage="CHALLENGING", content="Challenge premature consensus and hidden incentives."))
    runtime.transition_to(InquiryState.SYNTHESISING)
    runtime.contribute(Contribution(agent="Sael", stage="SYNTHESISING", content="Propose a provisional synthesis for review."))
    runtime.transition_to(InquiryState.REVIEWING)
    runtime.transition_to(InquiryState.CLOSED)

    print(f"Inquiry {envelope.id} completed. Ledger written to .ledger/{envelope.id}.jsonl")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
