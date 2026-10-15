# ADR 0002: Set visual tolerance at 1% changed pixels

## Context

Visual snapshots can fail for meaningful regressions or harmless rendering noise. A zero-tolerance threshold makes contributors distrust the suite.

## Decision

Use Playwright screenshots with `maxDiffPixelRatio: 0.01` for the checklist card.

## Consequences

The threshold catches layout and color changes while allowing small antialiasing differences. The false-negative cost is that a very small visual defect may pass. The false-positive cost of a lower threshold is higher for this portfolio because it would train maintainers to update snapshots without review.
