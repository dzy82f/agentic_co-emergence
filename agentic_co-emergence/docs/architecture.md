# Architecture: Agentic Reasoning v0.1

## Purpose

Agentic Reasoning creates a governed environment in which multiple reasoning agents improve collective understanding before judgement or decision.

## Frozen concepts for v0.1

### 1. Inquiry Envelope

The Inquiry Envelope is the bounded problem space. It defines:

- the question under inquiry;
- the domain or problem envelope;
- constraints;
- required perspectives;
- success criteria;
- minimum reasoning depth before synthesis.

The Inquiry Envelope is not the answer. It is the governed container for reasoning.

### 2. Formal Organisation

The Formal Organisation owns the process. It is responsible for:

- opening an inquiry;
- defining or approving the Inquiry Envelope;
- enforcing protocol boundaries;
- authorising transitions;
- accepting or rejecting synthesis;
- closing the inquiry.

It does not replace the Reasoning Community.

### 3. Reasoning Community

The Reasoning Community is the set of agents invited to reason within the Inquiry Envelope. It contributes perspectives, challenges assumptions and expands understanding.

It does not own governance.

### 4. Runtime

The Runtime enforces state. At any point, only the protocol relevant to the current state is available. Invalid transitions are rejected.

The Runtime is deliberately simple in v0.1.

### 5. Ledger

The Ledger records the history of the inquiry:

- inquiry creation;
- agent contributions;
- state transitions;
- synthesis attempts;
- review outcomes;
- closure.

The Ledger is the basis for audit, review and later analytics.

## v0.1 State Model

```text
DRAFT -> OPEN -> EXPLORING -> CHALLENGING -> SYNTHESISING -> REVIEWING -> CLOSED
```

Invalid transitions must fail.

## Non-goals for v0.1

- No autonomous agent orchestration.
- No LLM provider integration.
- No web application.
- No database dependency.
- No elaborate analytics.
- No speculative protocol expansion.

v0.1 should prove the governed reasoning structure before adding intelligence around it.
