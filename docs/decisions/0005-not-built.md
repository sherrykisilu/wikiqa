# ADR 0005: What was deliberately not built

## Context

A portfolio repository can become broad and shallow if every relevant technology is represented equally.

## Decision

Do not build a large extension, a custom visual-diff engine, a hosted metrics dashboard, or a full MediaWiki release workflow.

## Consequences

The repository stays reviewable. The tradeoff is that it demonstrates quality system design around one small extension rather than breadth across many product surfaces.
