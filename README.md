# WikiQA

MediaWiki extension teams often have two kinds of quality evidence: a wiki page that says what should be tested, and CI jobs that say whether a subset of it still works. The gap is where release risk hides: visual regressions are argued manually, documentation coverage is assumed rather than measured, and service-level metrics are reconstructed after an incident.

WikiQA is a small portfolio repository that treats that gap as the product. It contains one modest MediaWiki extension and the quality system around it: PHPUnit, Playwright E2E and visual regression tests, docs-as-code checks, and a Python metrics CLI for QA service reporting.

## What is in the repository

- `extension/`: a real MediaWiki parser-function extension. `{{#qaChecklist: Release readiness | ready}}` renders a consistent release-readiness checklist card.
- `tests/e2e/`: Playwright tests that create a page in MediaWiki, exercise the parser function, and compare a visual baseline with a 1% maximum changed-pixel ratio.
- `docs/`: MkDocs documentation, markdownlint, Vale plain-language rules, and a coverage gate for public PHP APIs and i18n messages.
- `metrics/`: a Python CLI that reports pass rate, flake rate, mean time to fix, automation coverage, and SLA attainment from JUnit, GitHub issue data, and a manual-test register.
- `manual-tests/`: manual cases with `migration_status` so manual-to-automation progress is tracked rather than narrated.

## Quickstart

```powershell
npm ci
py -m pip install -e .[dev]
py -m pytest metrics\tests
py scripts\docs_coverage.py --threshold 100
```

To run MediaWiki locally, Docker is required:

```powershell
docker compose up -d database mediawiki
docker compose exec -T mediawiki php maintenance/install.php --dbserver database --dbname mediawiki --dbuser wiki --dbpass wiki --server http://localhost:8080 --scriptpath "" --pass AdminPassword123! WikiQA Admin
docker compose exec -T mediawiki sh -lc "printf '\nwfLoadExtension( \'WikiQA\' );\n' >> LocalSettings.php"
npx playwright install --with-deps chromium
npx playwright test
```

Update visual baselines only after reviewing the rendered change:

```powershell
npx playwright test --update-snapshots
```

## Local verification on 2026-10-15

This Windows host has Node.js and the Python launcher, but it does not have PHP, Composer, Docker, or Docker Compose. I
verified the parts that do not require those missing runtimes and left the runtime-dependent checks to GitHub Actions.

| Check | Result | Runtime |
| --- | --- | --- |
| Metrics unit tests | 2 passed in 0.09 seconds | `py -m pytest metrics\tests` |
| Documentation coverage | 10/10 documented, 100 percent | `py scripts\docs_coverage.py --threshold 100` |
| Markdown and Vale linting | 13 Markdown files, 0 errors | `npm run docs:lint` |
| MkDocs build | strict build passed in 2.42 seconds | `py -m mkdocs build --strict` |
| Playwright discovery | 3 tests discovered | `npx playwright test --list` |
| PHP lint and PHPUnit | Not run locally; PHP is absent | GitHub Actions `PHP` workflow |
| Docker MediaWiki E2E | Not run locally; Docker is absent | GitHub Actions `E2E and visual regression` workflow |

## Results from the checked-in sample run

The metrics fixtures describe a small service slice rather than a made-up dashboard:

| Metric | Value | Target | Status |
| --- | ---: | ---: | --- |
| Test pass rate | 83.33% | 95% | missed |
| Flake rate | 16.67% | 2% | missed |
| Mean time to fix | 36.00 hours | 48 hours | met |
| Automation coverage | 50.00% | 70% | missed |
| SLA attainment | 25.00% | 100% | missed |

That is deliberate. A useful quality tool should expose uncomfortable gaps early: one flaky E2E test, two manual cases still in transition, and a pass-rate target that cannot be claimed from partial evidence.

## What I deliberately did not build

- A broad MediaWiki product clone. The extension is small so the quality system can be reviewed end to end.
- A custom screenshot comparator. Playwright already owns that problem; this repository documents the tolerance and uses the tool directly.
- A vanity dashboard. The metrics CLI emits text and JSON so CI, GitHub Pages, or a future service can consume the same calculations.
- A pretend all-green sample. The sample data contains misses because service metrics are only useful when they can say no.
