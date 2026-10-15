from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def public_php_symbols() -> set[str]:
    symbols: set[str] = set()
    for path in (ROOT / "extension" / "includes").glob("*.php"):
        text = path.read_text(encoding="utf-8")
        class_match = re.search(r"class\s+(\w+)", text)
        if not class_match:
            continue
        class_name = class_match.group(1)
        symbols.add(class_name)
        for method in re.findall(r"public\s+(?:static\s+)?function\s+(\w+)", text):
            symbols.add(f"{class_name}::{method}")
    return symbols


def i18n_keys() -> set[str]:
    data = json.loads((ROOT / "extension" / "i18n" / "en.json").read_text(encoding="utf-8"))
    return {key for key in data if key != "@metadata"}


def docs_text() -> str:
    return "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "docs").rglob("*.md"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--threshold", type=float, default=100.0)
    args = parser.parse_args()

    required = public_php_symbols() | i18n_keys()
    text = docs_text()
    documented = {item for item in required if item in text}
    coverage = (len(documented) / len(required) * 100) if required else 100.0
    missing = sorted(required - documented)

    print(f"Docs coverage: {coverage:.2f}% ({len(documented)}/{len(required)})")
    if missing:
        print("Missing documentation entries:")
        for item in missing:
            print(f"- {item}")
    return 0 if coverage >= args.threshold else 1


if __name__ == "__main__":
    raise SystemExit(main())
