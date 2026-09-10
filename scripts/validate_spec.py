#!/usr/bin/env python3
"""Validate a spec directory against design/HUMAN_SPECS.md and design/AGENT_TASKING.md.

Checks the human spec (microspec.md) and, when present, the agent's agent_tasking.md beside it.

Usage:
    python3 validate_spec.py <spec-dir> [<spec-dir> ...]
    python3 validate_spec.py specs/20260908-my-task/microspec.md   # file path also accepted

Exit codes:
    0 = all checks passed
    1 = violations found
"""

import re
import sys
import argparse
from pathlib import Path

TASKING_FILE = "agent_tasking.md"
DIR_NAME_RE = re.compile(r"^\d{8}-[a-z0-9][a-z0-9-]*$")
HEADING_RE = re.compile(r"^(#{1,3})\s+(.*\S)\s*$")
CHECK_ID_RE = re.compile(r"^- \[[ x]\] \**([RUTAXS])(\d+)\b")
TRACKER_RE = re.compile(r"\bDONE\b|\bStatus:|\bREVERTED\b|NOT IMPLEMENTED|at spec phase")
LINE_NUMBER_REF_RE = re.compile(r"\b[\w./-]+\.[A-Za-z]{1,5}:\d+\b")

LAYOUT = ["problem", "requirements", "scope", "implementation approach", "implementation tasks", "acceptance criteria", "verification", "related"]
SPEC_FILE = "microspec.md"
AGENT_SECTIONS = ["task breakdown", "test plan", "security checklist"]
TASKING_REQUIRED = ["task breakdown", "test plan", "security checklist"]
HUMAN_ONLY_SECTIONS = ["requirements", "acceptance criteria"]
DEFAULT_S = [f"S{i}" for i in range(1, 11)]


class Violation:
    def __init__(self, path, message):
        self.path = path
        self.message = message

    def __str__(self):
        return f"  FAIL  {self.path}: {self.message}"


def normalize_heading(text):
    text = re.sub(r"^\d+\.\s*", "", text)
    text = re.sub(r"\s*\(.*?\)\s*", " ", text)
    return " ".join(text.lower().split())


def parse_sections(lines):
    sections, current = [], None
    for line in lines:
        m = HEADING_RE.match(line)
        if m and len(m.group(1)) >= 2:
            current = (normalize_heading(m.group(2)), len(m.group(1)), [])
            sections.append(current)
        elif current is not None:
            current[2].append(line)
    return sections


def has_section(sections, keyword):
    return any(keyword in name for name, _, _ in sections)


def section_body(sections, keyword):
    return [l for name, _, lines in sections if keyword in name for l in lines]


def check_ids(lines, prefix):
    return [int(m.group(2)) for l in lines if (m := CHECK_ID_RE.match(l)) and m.group(1) == prefix]


def common_prose_checks(path, lines, violations):
    for i, l in enumerate(lines, 1):
        if l.lstrip().startswith("```"):
            continue
        if TRACKER_RE.search(l):
            violations.append(Violation(path, f"line {i}: tracker marker in spec prose (HUMAN_SPECS.md § The spec is not a tracker)"))
        if LINE_NUMBER_REF_RE.search(l):
            violations.append(Violation(path, f"line {i}: line-number citation — use durable references (HUMAN_SPECS.md § Every tier)"))


def field_lines(lines, key):
    return [l for l in lines if re.match(rf"^\**{re.escape(key)}:\**\s*\S", l)]


def validate_layout(path, violations):
    """Every human spec file: What/When/Owner header, the eight sections in order, and their contents."""
    lines = path.read_text(encoding="utf-8").splitlines()
    sections = parse_sections(lines)
    for key in ("What", "When", "Owner"):
        n = len(field_lines(lines, key))
        if n != 1:
            violations.append(Violation(path, f"header must carry '**{key}:** <text>' exactly once before '## Problem' (found {n}) (HUMAN_SPECS.md § Every tier)"))
    names = [name for name, level, _ in sections if level == 2]
    if names != LAYOUT:
        violations.append(Violation(path, f"sections must be exactly {[n.title() for n in LAYOUT]} in order (found: {[n.title() for n in names]}) (HUMAN_SPECS.md § Layout)"))
    for key in ("Decision", "Success", "Next"):
        if not field_lines(section_body(sections, "problem"), key):
            violations.append(Violation(path, f"Problem must carry '**{key}:**'"))
    scope = "\n".join(section_body(sections, "scope")).lower()
    if "out of scope" not in scope:
        violations.append(Violation(path, "Scope must state what is out of scope"))
    if "boundary" not in scope:
        violations.append(Violation(path, "Scope must state the boundary — which modules change and which do not"))
    if "alternative" not in "\n".join(section_body(sections, "implementation approach")).lower():
        violations.append(Violation(path, "Implementation approach must name the alternatives considered and why not"))
    r_ids = check_ids(section_body(sections, "requirements"), "R")
    if not r_ids:
        violations.append(Violation(path, "Requirements — expected '- [ ] **R<n> — <title>:** ...' lines"))
    elif len(r_ids) != len(set(r_ids)):
        violations.append(Violation(path, "duplicate R ids"))
    ac_lines = [l for l in section_body(sections, "acceptance criteria") if re.match(r"^- \[[ x]\] \**AC\d+\b", l)]
    if not ac_lines:
        violations.append(Violation(path, "Acceptance Criteria — expected '- [ ] AC<n>: ...' lines"))
    else:
        cited = {int(n) for l in ac_lines for n in re.findall(r"\bR(\d+)\b", l)}
        missing = sorted(set(r_ids) - cited)
        if missing:
            violations.append(Violation(path, f"requirements with no acceptance criterion citing them: {['R%d' % n for n in missing]}"))
    for kw in AGENT_SECTIONS:
        if has_section(sections, kw):
            violations.append(Violation(path, f"section '{kw}' is agent-authored and belongs in {TASKING_FILE}"))
    common_prose_checks(path, lines, violations)
    return set(r_ids)


def validate_tasking_file(path, spec_r_ids, violations):
    lines = path.read_text(encoding="utf-8").splitlines()
    text = "\n".join(lines)
    sections = parse_sections(lines)
    for kw in TASKING_REQUIRED:
        if not has_section(sections, kw):
            violations.append(Violation(path, f"tasking file is missing section '{kw}' (AGENT_TASKING.md § Tasking file)"))
    for kw in HUMAN_ONLY_SECTIONS:
        if has_section(sections, kw):
            violations.append(Violation(path, f"section '{kw}' is human-authored and belongs in the spec — the tasking file references R<id>, it does not restate them"))
    a_ids = check_ids(lines, "A")
    if not a_ids:
        violations.append(Violation(path, "no task breakdown — expected '- [ ] A<n>: ...' lines"))
    elif len(a_ids) != len(set(a_ids)):
        violations.append(Violation(path, "duplicate A ids"))
    present_s = {f"S{i}" for i in check_ids(lines, "S")}
    missing_s = [s for s in DEFAULT_S if s not in present_s]
    if missing_s:
        violations.append(Violation(path, f"security checklist missing default items: {missing_s}"))
    referenced = {int(n) for n in re.findall(r"\bR(\d+)\b", text)}
    uncovered = sorted(spec_r_ids - referenced)
    if uncovered:
        violations.append(Violation(path, f"requirements not referenced by any task or test: {['R%d' % i for i in uncovered]}"))
    common_prose_checks(path, lines, violations)


def validate_spec_dir(spec_dir):
    violations = []
    spec_dir = Path(spec_dir)
    if spec_dir.is_file():
        spec_dir = spec_dir.parent
    if not spec_dir.is_dir():
        return [Violation(spec_dir, "not a directory")]
    if not DIR_NAME_RE.match(spec_dir.name):
        violations.append(Violation(spec_dir, "directory name must be <YYYYMMDD>-<slug> under specs/ (HUMAN_SPECS.md § File location)"))

    spec = spec_dir / SPEC_FILE
    if not spec.exists():
        violations.append(Violation(spec_dir, f"no {SPEC_FILE} (HUMAN_SPECS.md § File location)"))
        return violations
    r_ids = validate_layout(spec, violations)

    tasking = spec_dir / TASKING_FILE
    if tasking.exists():
        validate_tasking_file(tasking, r_ids, violations)
    return violations


def main():
    parser = argparse.ArgumentParser(description="Validate spec directories against design/HUMAN_SPECS.md and design/AGENT_TASKING.md")
    parser.add_argument("paths", nargs="+", help="spec directory (or a file inside it)")
    args = parser.parse_args()
    total = 0
    for p in args.paths:
        violations = validate_spec_dir(p)
        name = Path(p).name if Path(p).is_dir() else Path(p).parent.name
        if violations:
            print(f"\n{name}  ({len(violations)} violations)")
            for v in violations:
                print(str(v))
            total += len(violations)
        else:
            print(f"{name}  OK")
    print(f"\n{'='*60}")
    print(f"Checked {len(args.paths)} spec(s), {total} violation(s)")
    return 1 if total > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
