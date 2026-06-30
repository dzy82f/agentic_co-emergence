# Agentic Co-Emergence Research Questions

This document defines the research agenda for the Agentic Co-Emergence programme.

Research questions are organised into milestones. Each milestone contributes to both the theoretical framework and the runtime implementation.

---

# Research Discipline

Every research cycle must identify both a scientific objective and an engineering objective.

A theoretical question should only be pursued if answering it has the potential to influence the design, implementation, governance, testing, or evaluation of the runtime.

Every research cycle should therefore identify:

- the research question;
- the motivation for asking it;
- the engineering driver;
- the expected impact on the runtime;
- the repository artefacts expected to change.

This discipline ensures that theoretical work remains connected to the practical objective of building an executable Agentic Co-Emergence runtime.

---

# Milestone 001 — Towards a Computational Theory of Understanding

## Research Objectives

RQ-001: What is understanding?

RQ-002: How does understanding differ from knowledge, information, and belief?

RQ-003: What properties must an understanding possess?

RQ-004: What transformations can legitimately be applied to an understanding?

RQ-005: How can changes in understanding be observed or measured?

RQ-006: How do multiple understandings co-emerge?

RQ-007: How should understandings be governed?

RQ-008: How should understanding be represented computationally?

---

# Research Cycle 001

## Research Question

What is the smallest computational object that still deserves to be called an understanding?

## Motivation

The runtime requires a primary computational object.

Before implementing that object, we must determine the minimum properties required for something to constitute an understanding.

## Engineering Driver

The answer will determine the design of the runtime's core computational object.

Without this definition, it is impossible to specify:

- what state the runtime maintains;
- which transformations are legitimate;
- what should be version controlled;
- what experiments should observe.

## Initial Hypothesis

Understanding cannot be represented solely as information.

## Experimental Question

If essential properties are removed one by one from an understanding, at what point does it cease to be an understanding?

## Expected Runtime Impact

The outcome of this research cycle is expected to influence:

- Understanding
- Transformation
- Dialogue
- Governance

## Repository Artefacts

The following artefacts are expected to evolve during this research cycle:

- `docs/ontology.md`
- `docs/computational_model.md`
- `paper/body_v0.1.tex`
- `agentic_co_emergence/models/` *(when implementation begins)*
- `tests/` *(when implementation begins)*

---

# Future Research Cycles

Subsequent research cycles will extend or challenge the results of earlier cycles.

The objective is not simply to answer research questions, but to progressively develop a computational theory whose implementation can be validated experimentally.