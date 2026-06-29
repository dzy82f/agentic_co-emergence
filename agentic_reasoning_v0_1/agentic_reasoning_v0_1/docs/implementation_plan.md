# Implementation Plan

## Build order

1. Define typed models.
2. Implement the state machine.
3. Implement the runtime.
4. Implement the ledger.
5. Add CLI execution.
6. Add tests.
7. Run real inquiries.

## Engineering standards

- Keep the runtime deterministic.
- Keep state transitions explicit.
- Record every meaningful event.
- Prefer small modules over clever abstractions.
- Do not add an LLM dependency in v0.1.
- Do not allow synthesis before required reasoning stages.

## Acceptance criteria for v0.1

The repository is acceptable when:

- an inquiry can be loaded from YAML;
- an inquiry can move through the required states;
- invalid transitions fail clearly;
- contributions are recorded;
- synthesis is blocked until exploration and challenge have occurred;
- the final ledger is human-readable.
