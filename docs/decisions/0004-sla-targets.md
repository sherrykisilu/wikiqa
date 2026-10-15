# ADR 0004: Choose explicit QA service targets

## Context

A centralized quality services team needs targets that are strict enough to guide decisions and simple enough to explain.

## Decision

Use these defaults: 95% pass rate, 2% flake rate, 48-hour mean time to fix, and 70% automation coverage.

## Consequences

The targets are not universal. They are a starting operating contract. The important choice is that targets live in code and reports, so changes require review instead of being edited in a slide after the fact.
