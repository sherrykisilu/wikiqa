from __future__ import annotations

import argparse
import json
from pathlib import Path

from wikiqa_metrics.core import calculate_metrics, format_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Report QA service metrics from test and issue evidence."
    )
    parser.add_argument(
        "--junit", action="append", type=Path, required=True, help="JUnit XML file."
    )
    parser.add_argument(
        "--manual-register", type=Path, required=True, help="Manual test register YAML."
    )
    parser.add_argument(
        "--issues", type=Path, required=True, help="GitHub issue or PR evidence JSON."
    )
    parser.add_argument("--format", choices=["text", "json"], default="text")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    metrics = calculate_metrics(args.junit, args.manual_register, args.issues)
    if args.format == "json":
        print(json.dumps(metrics, indent=2, sort_keys=True))
    else:
        print(format_text(metrics))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
