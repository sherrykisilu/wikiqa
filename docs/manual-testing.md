# Manual testing register

Manual testing is not treated as a failure. Undocumented manual testing is the failure mode.

`manual-tests/register.yml` gives each manual case an owner, area, and `migration_status`:

- `manual`: the case is still intentionally manual.
- `in_progress`: the case has a known path to automation but is not done.
- `automated`: the case is represented by a checked-in automated test.

The metrics CLI uses this register for automation coverage. That means the transition from manual testing to automation is measured as an operating metric, not described only in a retrospective.
