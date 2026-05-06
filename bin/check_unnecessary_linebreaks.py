#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path


MD_LIST_RE = re.compile(r"^\s*(?:[-*+]\s+|\d+\.\s+)")


def is_prose_line(line: str) -> bool:
    s = line.rstrip("\n")
    t = s.strip()
    if not t:
        return False
    if t.startswith(("```", "~~~", "#", ">", "|")):
        return False
    if MD_LIST_RE.match(t):
        return False
    if s.startswith("    ") or s.startswith("\t"):
        return False
    return True


def find_unnecessary_breaks(path: Path) -> list[tuple[int, str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    hits: list[tuple[int, str, str]] = []
    in_fence = False
    fence = ""

    for i in range(len(lines) - 1):
        a = lines[i]
        b = lines[i + 1]
        ta = a.strip()
        tb = b.strip()

        if ta.startswith("```") or ta.startswith("~~~"):
            marker = "```" if ta.startswith("```") else "~~~"
            if not in_fence:
                in_fence = True
                fence = marker
            elif marker == fence:
                in_fence = False
                fence = ""
            continue

        if in_fence:
            continue

        if is_prose_line(a) and is_prose_line(b):
            hits.append((i + 1, a.strip(), b.strip()))

    return hits


def iter_md_files(inputs: list[str]) -> list[Path]:
    if inputs:
        out: list[Path] = []
        for item in inputs:
            p = Path(item)
            if p.is_dir():
                out.extend(sorted(p.rglob("*.md")))
            elif p.is_file():
                out.append(p)
        return sorted(set(out))
    return sorted(Path(".").rglob("*.md"))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Find likely unnecessary hard line breaks in markdown prose."
    )
    parser.add_argument("paths", nargs="*", help="Files or directories to scan")
    args = parser.parse_args()

    files = iter_md_files(args.paths)
    total_hits = 0

    for file in files:
        hits = find_unnecessary_breaks(file)
        for line_no, left, right in hits:
            total_hits += 1
            print(f"{file}:{line_no}: {left}\\n{right}")

    if total_hits == 0:
        print("No likely unnecessary line breaks found.")
        return 0

    print(f"Found {total_hits} likely unnecessary line break(s).")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

