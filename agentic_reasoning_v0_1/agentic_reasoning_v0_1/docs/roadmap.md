# Development Roadmap

## Phase 1: Architecture Freeze

Deliverables:

- frozen v0.1 concept model;
- state model;
- repository structure;
- initial runtime contract;
- example inquiry envelope.

Exit condition:

- the runtime can open, advance and close a governed inquiry using explicit transitions.

## Phase 2: Runtime Skeleton

Deliverables:

- typed models;
- state machine;
- transition validation;
- file-backed ledger;
- CLI runner;
- basic tests.

Exit condition:

- invalid transitions are rejected;
- all events are recorded.

## Phase 3: Protocol Enforcement

Deliverables:

- minimum contribution requirements;
- no synthesis before exploration and challenge;
- explicit review before closure.

Exit condition:

- the runtime enforces understanding-before-judgement.

## Phase 4: Real Inquiry Tests

Deliverables:

- at least three real inquiry examples;
- review notes;
- failure cases;
- v0.2 backlog.

Exit condition:

- v0.1 is useful enough to structure real reasoning sessions.

## Phase 5: v0.2 Scoping

Only after v0.1 has been tested should v0.2 be considered.

Candidate v0.2 items:

- agent handoff logic;
- richer ledger analytics;
- protocol modules;
- persistent database;
- web UI integration;
- Issue Studio integration.
