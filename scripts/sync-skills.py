#!/usr/bin/env python3
"""Synchronize canonical Agent Skills into tool-specific directories."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "canonical"
TARGETS = (ROOT / "claude", ROOT / "codex", ROOT / "copilot")


def skill_names(base: Path) -> set[str]:
    if not base.is_dir():
        return set()
    return {
        child.name
        for child in base.iterdir()
        if child.is_dir() and (child / "SKILL.md").is_file()
    }


def compare_directories(expected: Path, actual: Path) -> list[str]:
    if not actual.is_dir():
        return [f"missing directory: {actual.relative_to(ROOT)}"]

    problems: list[str] = []
    expected_files = {
        path.relative_to(expected) for path in expected.rglob("*") if path.is_file()
    }
    actual_files = {
        path.relative_to(actual) for path in actual.rglob("*") if path.is_file()
    }

    for path in sorted(expected_files - actual_files):
        problems.append(f"missing: {(actual / path).relative_to(ROOT)}")
    for path in sorted(actual_files - expected_files):
        problems.append(f"unexpected: {(actual / path).relative_to(ROOT)}")
    for path in sorted(expected_files & actual_files):
        if (expected / path).read_bytes() != (actual / path).read_bytes():
            problems.append(f"differs: {(actual / path).relative_to(ROOT)}")
    return problems


def check() -> int:
    canonical_names = skill_names(CANONICAL)
    if not canonical_names:
        print("No canonical skills found.", file=sys.stderr)
        return 1

    problems: list[str] = []
    for target in TARGETS:
        target_names = skill_names(target)
        for name in sorted(canonical_names - target_names):
            problems.append(f"missing generated skill: {(target / name).relative_to(ROOT)}")
        for name in sorted(target_names - canonical_names):
            problems.append(f"unexpected generated skill: {(target / name).relative_to(ROOT)}")
        for name in sorted(canonical_names & target_names):
            problems.extend(compare_directories(CANONICAL / name, target / name))

    if problems:
        print("Generated skill copies are out of sync:", file=sys.stderr)
        for problem in problems:
            print(f"- {problem}", file=sys.stderr)
        print("Run: python3 scripts/sync-skills.py", file=sys.stderr)
        return 1

    print(
        f"All {len(canonical_names)} canonical skills are synchronized "
        f"across {len(TARGETS)} agent directories."
    )
    return 0


def sync() -> int:
    canonical_names = skill_names(CANONICAL)
    if not canonical_names:
        print("No canonical skills found.", file=sys.stderr)
        return 1

    for target in TARGETS:
        target.mkdir(parents=True, exist_ok=True)
        for stale_name in sorted(skill_names(target) - canonical_names):
            shutil.rmtree(target / stale_name)
            print(f"Removed stale generated skill: {(target / stale_name).relative_to(ROOT)}")
        for name in sorted(canonical_names):
            destination = target / name
            if destination.exists():
                shutil.rmtree(destination)
            shutil.copytree(CANONICAL / name, destination)
            print(f"Synchronized: {destination.relative_to(ROOT)}")

    return check()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify generated copies without modifying files",
    )
    args = parser.parse_args()
    return check() if args.check else sync()


if __name__ == "__main__":
    raise SystemExit(main())
