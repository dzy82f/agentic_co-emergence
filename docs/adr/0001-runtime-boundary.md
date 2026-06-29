# ADR 0001: Runtime Boundary

## Status

Accepted

## Context

Agentic Reasoning requires a governed environment in which reasoning activity is constrained by an explicit runtime rather than informal prompt discipline.

## Decision

The runtime is responsible for controlling state, enforcing valid transitions, recording events, and determining which protocols are available at each stage.

The reasoning community does not control the runtime. It operates within the boundary set by the formal system.

## Consequences

This separates governance from reasoning. It prevents accidental leakage between states and makes Agentic Reasoning testable as software rather than dependent on conversational discipline.
