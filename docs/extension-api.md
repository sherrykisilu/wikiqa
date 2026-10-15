# Extension API documentation

This page is intentionally explicit because `scripts/docs_coverage.py` gates public PHP APIs and i18n keys.

## Public PHP classes and methods

- `Hooks`: registers WikiQA with MediaWiki parser lifecycle hooks.
- `Hooks::onParserFirstCallInit`: attaches the `qaChecklist` parser function to a `MediaWiki\Parser\Parser` instance.
- `ChecklistRenderer`: builds the checklist card HTML returned by the parser function.
- `ChecklistRenderer::render`: accepts the parser, title, and status; adds the ResourceLoader style module; escapes user-provided text; and returns MediaWiki parser-function output.
- `ChecklistRenderer::normaliseStatus`: constrains status input to `draft`, `ready`, or `blocked`, with `draft` as the safe fallback.

## i18n message keys

- `wikiqa-desc`: extension description for `Special:Version`.
- `wikiqa-checklist-title`: default checklist heading.
- `wikiqa-status-draft`: user-facing draft status label.
- `wikiqa-status-ready`: user-facing ready status label.
- `wikiqa-status-blocked`: user-facing blocked status label.

## Parser function contract

The parser function is:

```wikitext
{{#qaChecklist: title | status}}
```

`status` accepts `draft`, `ready`, or `blocked`. Unknown values render as `draft` so a typo does not create a fourth undocumented state.
