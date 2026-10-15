from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import statistics
import xml.etree.ElementTree as ET

import yaml


@dataclass(frozen=True)
class SlaTargets:
    pass_rate: float = 0.95
    flake_rate: float = 0.02
    mttr_hours: float = 48.0
    automation_coverage: float = 0.70


def _parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def read_junit(paths: list[Path]) -> list[dict[str, object]]:
    cases: list[dict[str, object]] = []
    for path in paths:
        root = ET.parse(path).getroot()
        for case in root.iter("testcase"):
            failed = case.find("failure") is not None or case.find("error") is not None
            skipped = case.find("skipped") is not None
            properties = {
                prop.attrib.get("name", ""): prop.attrib.get("value", "")
                for prop in case.findall("./properties/property")
            }
            cases.append(
                {
                    "name": f"{case.attrib.get('classname', '')}.{case.attrib.get('name', '')}",
                    "failed": failed,
                    "skipped": skipped,
                    "flaky": properties.get("flaky", "false").lower() == "true",
                    "time": float(case.attrib.get("time", "0") or 0),
                    "source": str(path),
                }
            )
    return cases


def read_manual_register(path: Path) -> list[dict[str, object]]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return list(data["cases"])


def read_issue_data(path: Path) -> list[dict[str, object]]:
    return json.loads(path.read_text(encoding="utf-8"))


def calculate_metrics(
    junit_paths: list[Path], manual_register: Path, issue_data: Path, targets: SlaTargets | None = None
) -> dict[str, object]:
    targets = targets or SlaTargets()
    cases = read_junit(junit_paths)
    manual_cases = read_manual_register(manual_register)
    issues = read_issue_data(issue_data)

    executed = [case for case in cases if not case["skipped"]]
    passed = [case for case in executed if not case["failed"]]
    flaky = [case for case in executed if case["flaky"]]
    automated_manual = [case for case in manual_cases if case["migration_status"] == "automated"]
    fix_hours = [
        (_parse_time(issue["fixed_at"]) - _parse_time(issue["opened_at"])).total_seconds() / 3600
        for issue in issues
        if issue.get("fixed_at")
    ]

    pass_rate = len(passed) / len(executed) if executed else 0.0
    flake_rate = len(flaky) / len(executed) if executed else 0.0
    mttr = statistics.mean(fix_hours) if fix_hours else 0.0
    coverage = len(automated_manual) / len(manual_cases) if manual_cases else 0.0

    checks = {
        "pass_rate": pass_rate >= targets.pass_rate,
        "flake_rate": flake_rate <= targets.flake_rate,
        "mean_time_to_fix_hours": mttr <= targets.mttr_hours,
        "automation_coverage": coverage >= targets.automation_coverage,
    }

    return {
        "test_count": len(executed),
        "passed_count": len(passed),
        "failed_count": len([case for case in executed if case["failed"]]),
        "flaky_count": len(flaky),
        "manual_case_count": len(manual_cases),
        "automated_manual_case_count": len(automated_manual),
        "pass_rate": pass_rate,
        "flake_rate": flake_rate,
        "mean_time_to_fix_hours": mttr,
        "automation_coverage": coverage,
        "sla_checks": checks,
        "sla_attainment": sum(1 for value in checks.values() if value) / len(checks),
        "targets": {
            "pass_rate": targets.pass_rate,
            "flake_rate": targets.flake_rate,
            "mean_time_to_fix_hours": targets.mttr_hours,
            "automation_coverage": targets.automation_coverage,
        },
    }


def format_text(metrics: dict[str, object]) -> str:
    targets = metrics["targets"]
    lines = ["WikiQA service metrics", "======================", ""]
    rows = [
        ("Test pass rate", metrics["pass_rate"], targets["pass_rate"], True),
        ("Flake rate", metrics["flake_rate"], targets["flake_rate"], False),
        ("Mean time to fix", metrics["mean_time_to_fix_hours"], targets["mean_time_to_fix_hours"], False),
        ("Automation coverage", metrics["automation_coverage"], targets["automation_coverage"], True),
        ("SLA attainment", metrics["sla_attainment"], 1.0, True),
    ]
    for label, value, target, higher_is_better in rows:
        if isinstance(value, float) and value <= 1 and label != "Mean time to fix":
            rendered_value = f"{value:.2%}"
            rendered_target = f"{target:.0%}"
        else:
            rendered_value = f"{value:.2f} hours"
            rendered_target = f"{target:.0f} hours"
        met = value >= target if higher_is_better else value <= target
        lines.append(f"- {label}: {rendered_value} (target {rendered_target}) — {'met' if met else 'missed'}")
    return "\n".join(lines)
