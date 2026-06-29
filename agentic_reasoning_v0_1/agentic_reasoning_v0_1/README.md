# Agentic Reasoning v0.1

Agentic Reasoning is a governed environment for collective reasoning. Its purpose is to improve understanding before judgement or decision.

This repository is the first production implementation. It is not a continuation of the Tychevia Runtime prototypes v5-v8. Those prototypes informed the design, but this codebase begins cleanly.

## v0.1 Scope

v0.1 implements a minimal governed reasoning runtime:

1. An Inquiry Envelope defines the question, domain, constraints and success criteria.
2. A Formal Organisation owns governance, state transitions and closure.
3. A Reasoning Community contributes perspectives within the active protocol.
4. A Runtime enforces the current state and prevents invalid transitions.
5. A Ledger records every event, contribution and transition.

## Core principle

Understanding precedes judgement.

The runtime should not permit synthesis, decision or closure until the required reasoning stages have occurred.

## Quick start

```bash
python -m agentic_reasoning.cli.run examples/ethical_governance_inquiry.yaml
```

## Repository layout

```text
agentic_reasoning/        Runtime package
  core/                   State machine, runtime and governance
  models/                 Domain models
  protocols/              Stage protocols
  storage/                Ledger persistence
  cli/                    Command line entry points
docs/                     Architecture and roadmap
examples/                 Example inquiry envelopes
inquiries/                Working inquiry files
tests/                    Runtime tests
```

## Status

v0.1 scaffold. Production hardening begins after architecture freeze.
