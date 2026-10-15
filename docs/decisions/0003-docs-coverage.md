# ADR 0003: Gate documentation coverage in CI

## Context

MediaWiki extensions expose behavior through PHP APIs and i18n messages. Missing documentation usually appears later as support load.

## Decision

Fail CI when public PHP classes, public methods, or i18n message keys are not documented in `docs/`.

## Consequences

This creates maintenance friction for small code changes. That friction is intentional: documentation debt is cheaper when it is attached to the change that created it.
