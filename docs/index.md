# WikiQA toolkit

WikiQA demonstrates a narrow MediaWiki extension and the quality practices around it. The extension is intentionally small: the test subject is a release-readiness checklist card, not a second wiki product.

The quality system is the larger artifact. It shows how an extension team can connect automated checks, visual review, documentation coverage, manual test migration, and QA service metrics without hiding the cost of those choices.

## Extension behavior

Editors can add a checklist card with:

```wikitext
{{#qaChecklist: Release readiness | ready}}
```

The parser function renders a checklist with documented acceptance criteria, coverage linkage, and release-evidence ownership.

## Quality gates

- PHPUnit covers parser hook registration and renderer behavior.
- Playwright covers the editor-visible flow in a Docker MediaWiki instance.
- Playwright visual snapshots compare the checklist card with a 1% maximum changed-pixel ratio.
- markdownlint and Vale keep documentation plain and consistent.
- `scripts/docs_coverage.py` requires 100% documentation coverage for public PHP APIs and i18n keys.
- `wikiqa-metrics` reports pass rate, flake rate, mean time to fix, automation coverage, and SLA attainment.
