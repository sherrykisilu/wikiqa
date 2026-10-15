# QA service metrics

The metrics CLI is designed for a centralized quality services team that needs to report operating health, not only test counts.

## Inputs

- JUnit XML from PHPUnit and Playwright.
- GitHub issue or pull request evidence with `opened_at` and `fixed_at` fields.
- `manual-tests/register.yml`, including a `migration_status` for every manual case.

## Reported metrics

- Test pass rate: passed executed tests divided by executed tests.
- Flake rate: executed tests marked with the `flaky` property divided by executed tests.
- Mean time to fix: average hours between failure issue open and fix time.
- Automation coverage ratio: manual cases with `migration_status: automated` divided by all registered manual cases.
- SLA attainment: the share of metric targets met in the current report.

The default targets are deliberately stated in code: 95% pass rate, 2% flake rate, 48-hour mean time to fix, and 70% automation coverage.
