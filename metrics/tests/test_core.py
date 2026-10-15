from pathlib import Path

from wikiqa_metrics.core import calculate_metrics, format_text

FIXTURES = Path(__file__).parent / "fixtures"


def test_calculates_service_metrics_from_junit_manual_register_and_issues() -> None:
    metrics = calculate_metrics(
        [FIXTURES / "phpunit.xml", FIXTURES / "playwright.xml"],
        Path("manual-tests/register.yml"),
        FIXTURES / "issues.json",
    )

    assert metrics["test_count"] == 6
    assert metrics["passed_count"] == 5
    assert metrics["failed_count"] == 1
    assert metrics["pass_rate"] == 5 / 6
    assert metrics["flake_rate"] == 1 / 6
    assert metrics["mean_time_to_fix_hours"] == 36
    assert metrics["automation_coverage"] == 0.5
    assert metrics["sla_attainment"] == 0.25


def test_text_report_names_targets_and_status() -> None:
    metrics = calculate_metrics(
        [FIXTURES / "phpunit.xml", FIXTURES / "playwright.xml"],
        Path("manual-tests/register.yml"),
        FIXTURES / "issues.json",
    )

    report = format_text(metrics)

    assert "Test pass rate: 83.33% (target 95%) — missed" in report
    assert "Mean time to fix: 36.00 hours (target 48 hours) — met" in report
