```markdown
# Architecture

## Overview

Agentic Co-Emergence is organised into a number of layers.

The intention is to separate governance,
runtime execution,
domain knowledge,
and persistence.

---

## Package Overview

### cli

Responsible for launching the runtime.

Contains:

- run.py

---

### core

The orchestration layer.

Responsibilities:

- Runtime controller
- Prompt compilation
- Policy loading
- Validation
- State transitions

---

### engines

Provides computational services.

Includes:

- reasoning
- memory
- knowledge
- semantic graph

---

### personas

Defines the participating agents.

Contains:

- persona markdown
- persona manager

---

### protocols

Markdown protocols governing dialogue.

Examples:

- Constitution
- ADSN
- Review
- Startup

---

### projections

Creates external views of runtime state.

Examples:

- reasoning projection
- memory projection
- knowledge projection

---

### storage

Persistence layer.

Responsible for:

- event store
- conversation history
- telemetry

---

### models

Shared data structures.
