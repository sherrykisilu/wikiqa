# ADR 0001: Use Playwright for E2E and visual testing

## Context

The project needs browser E2E coverage and visual regression checks against a MediaWiki extension.

## Decision

Use Playwright rather than Selenium or Cypress.

## Consequences

Playwright gives first-class browser automation, trace collection, and screenshot comparison in one tool. The cost is that contributors need browser binaries and the tests must manage deterministic rendering. That cost is smaller than wiring separate tools for E2E and visual comparison.
