#!/usr/bin/env python3
"""Validate objective Meta Apollo Repository Grammar v1 invariants."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROOMS = ("ATLAS", "MODEL", "BUILD", "DEV", "OPERATE", "EVIDENCE", "ARCHIVE")
LINEAGE = "✦︎✦︎✦︎ Meta Apollo Logos //"
RAILS = (
    "focus-rail.svg",
    "nav-rail.svg",
    "model-rail.svg",
    "agency-rail.svg",
    "system-rail.svg",
    "scope-rail.svg",
    "warning-rail.svg",
    "neutral-rail.svg",
)
FENCE = chr(96) * 3


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def headings_outside_fences(text: str) -> list[tuple[int, str]]:
    headings: list[tuple[int, str]] = []
    in_fence = False
    for number, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith(FENCE):
            in_fence = not in_fence
            continue
        if not in_fence and re.match(r"^#{1,6}\s+", line):
            headings.append((number, line))
    return headings


def exempt_paths(marker_text: str) -> set[str]:
    result: set[str] = set()
    active = False
    for line in marker_text.splitlines():
        if line.strip() == "validator_exempt:":
            active = True
            continue
        if active:
            match = re.match(r"^\s+-\s+(.+?)\s*$", line)
            if match:
                result.add(match.group(1))
                continue
            if line and not line.startswith((" ", "\t")):
                active = False
    return result


def main() -> int:
    errors: list[str] = []

    marker_text = read(ROOT / ".meta-apollo.yml")
    if not marker_text:
        errors.append("missing .meta-apollo.yml")
    elif not re.search(r"(?m)^design_language:\s*1\s*$", marker_text):
        errors.append(".meta-apollo.yml must declare design_language: 1")

    exemptions = exempt_paths(marker_text)

    root_text = read(ROOT / "README.md")
    if not root_text:
        errors.append("missing README.md")
    else:
        if not root_text.startswith(LINEAGE):
            errors.append("README.md must begin with the Meta Apollo lineage marker")
        if "> **STATE //**" not in root_text:
            errors.append("README.md is missing the compact metadata chassis")
        h1s = [h for _, h in headings_outside_fences(root_text) if h.startswith("# ")]
        if len(h1s) != 1:
            errors.append(f"README.md must have exactly one H1; found {len(h1s)}")

    for room in ROOMS:
        room_dir = ROOT / room
        room_readme = room_dir / "README.md"
        if not room_dir.is_dir():
            errors.append(f"missing canonical room: {room}/")
            continue
        text = read(room_readme)
        if not text:
            errors.append(f"missing room map: {room}/README.md")
            continue
        if not text.startswith(LINEAGE):
            errors.append(f"{room}/README.md must begin with the Meta Apollo lineage marker")
        if f"MAP // {room}" not in text:
            errors.append(f"{room}/README.md is missing its MAP // {room} identity")
        if "> **STATE //**" not in text:
            errors.append(f"{room}/README.md is missing the compact metadata chassis")
        for target in ROOMS:
            if target not in text:
                errors.append(f"{room}/README.md navigation is missing {target}")
        if r"\~\~" not in text:
            errors.append(f"{room}/README.md navigation is missing Ghost String connectors")
        h1s = [h for _, h in headings_outside_fences(text) if h.startswith("# ")]
        if len(h1s) != 1:
            errors.append(f"{room}/README.md must have exactly one H1; found {len(h1s)}")

    chassis = ROOT / "BUILD" / "assets" / "design" / "chassis"
    for rail in RAILS:
        if not (chassis / rail).is_file():
            errors.append(f"missing chassis asset: BUILD/assets/design/chassis/{rail}")

    for md in ROOT.rglob("*.md"):
        rel = md.relative_to(ROOT).as_posix()
        if rel.startswith("ARCHIVE/") or rel.startswith("BUILD/templates/") or rel in exemptions:
            continue
        text = read(md)
        if "neutral-rail.svg" not in text:
            continue
        headings = headings_outside_fences(text)
        first_h1 = next((n for n, h in headings if h.startswith("# ")), None)
        second_heading = next((n for n, _ in headings if first_h1 and n > first_h1), None)
        neutral_lines = [i for i, line in enumerate(text.splitlines(), 1) if "neutral-rail.svg" in line]
        if len(neutral_lines) > 1:
            errors.append(f"{rel} has more than one off-white page chassis rail")
        if neutral_lines and second_heading and neutral_lines[0] > second_heading:
            errors.append(f"{rel} uses the off-white rail below a local section heading")

    if errors:
        print("META APOLLO REPOSITORY GRAMMAR // v1 // FAIL")
        for error in errors:
            print(f" - {error}")
        return 1

    print("META APOLLO REPOSITORY GRAMMAR // v1 // PASS")
    print("seven rooms · lineage · metadata · navigation · chassis · version")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
