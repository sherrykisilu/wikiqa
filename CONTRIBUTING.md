# Contributing

WikiQA follows the same bias as the code it demonstrates: small changes, documented tradeoffs, and evidence before assertion.

## Development setup

1. Install Node.js, Python 3.11+, PHP 8.1+, Composer, and Docker.
2. Run `npm ci`.
3. Run `py -m pip install -e .[dev]`.
4. For PHP tests, run `composer install` and then `vendor/bin/phpunit`.

## Pull request expectations

A pull request should include:

- the problem being solved;
- the test evidence produced locally or in CI;
- documentation updates for user-visible behavior, public PHP APIs, i18n messages, or metrics semantics;
- an ADR when a decision changes a quality threshold, tool, or operating model.

## Review style

Reviewers should block changes for correctness, maintainability, missing evidence, or undocumented tradeoffs. Preference alone is not enough; explain the operational cost of the alternative.

## Manual tests

When a manual case is added, include its `migration_status` and owner. If the case is a candidate for automation, state what blocks that migration.
