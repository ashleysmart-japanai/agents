#!/usr/bin/env python3
"""Validate a spec directory against design/HUMAN_SPECS.md and design/AGENT_TASKING.md.

Checks the human spec (micro-spec.md, quick-spec.md, or requirements.md/design.md/tasks.md)
and, when present, the agent's agent_tasking.md beside it.

Usage:
    python3 validate_spec.py <spec-dir> [<spec-dir> ...]
    python3 validate_spec.py specs/20260908-my-task/micro-spec.md   # file path also accepted

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

MICRO_FIELDS = ["What", "When", "Owner", "Why", "How", "Acceptance", "Not changing", "Alternatives"]
QUICK_SECTIONS = ["problem", "requirements", "implementation approach", "implementation tasks", "verification", "related"]
STANDARD_FILES = ["requirements.md", "design.md", "tasks.md"]
AGENT_SECTIONS = ["task breakdown", "test plan", "security checklist"]
TASKING_REQUIRED = ["task breakdown", "test plan", "security checklist"]
HUMAN_ONLY_SECTIONS = ["requirements", "acceptance checklist"]
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


def check_when_owner(path, lines, violations):
    for key in ("When", "Owner"):
        if len(field_lines(lines, key)) != 1:
            violations.append(Violation(path, f"must carry '**{key}:** <text>' exactly once (HUMAN_SPECS.md § Every tier)"))


def validate_micro(path, violations):
    lines = path.read_text(encoding="utf-8").splitlines()
    for key in MICRO_FIELDS:
        n = len(field_lines(lines, key))
        if n != 1:
            violations.append(Violation(path, f"micro spec must carry '**{key}:**' exactly once (found {n}) (HUMAN_SPECS.md § Micro spec)"))
    if not any(l.strip().lower().startswith("## related") for l in lines):
        violations.append(Violation(path, "micro spec is missing '## Related'"))
    sections = parse_sections(lines)
    for kw in AGENT_SECTIONS:
        if has_section(sections, kw):
            violations.append(Violation(path, f"section '{kw}' is agent-authored and belongs in {TASKING_FILE}"))
    common_prose_checks(path, lines, violations)
    return set()


def validate_quick(path, violations):
    lines = path.read_text(encoding="utf-8").splitlines()
    sections = parse_sections(lines)
    check_when_owner(path, lines, violations)
    for key in ("Decision", "Success", "Next"):
        if not field_lines(lines, key):
            violations.append(Violation(path, f"quick spec Problem block must carry '**{key}:**' (HUMAN_SPECS.md § Quick spec)"))
    for kw in QUICK_SECTIONS:
        if not has_section(sections, kw):
            violations.append(Violation(path, f"quick spec is missing section '{kw}' (HUMAN_SPECS.md § Quick spec)"))
    text = "\n".join(lines).lower()
    if "out of scope" not in text:
        violations.append(Violation(path, "quick spec must state what is out of scope"))
    if "boundary" not in text:
        violations.append(Violation(path, "quick spec must state the boundary — which modules change and which do not"))
    if "alternative" not in text:
        violations.append(Violation(path, "quick spec must name the alternatives considered and why not"))
    r_ids = check_ids(lines, "R")
    if not r_ids:
        violations.append(Violation(path, "no requirements — expected '- [ ] **R<n> — <title>:** ...' lines"))
    elif len(r_ids) != len(set(r_ids)):
        violations.append(Violation(path, "duplicate R ids"))
    for kw in AGENT_SECTIONS:
        if has_section(sections, kw):
            violations.append(Violation(path, f"section '{kw}' is agent-authored and belongs in {TASKING_FILE}"))
    common_prose_checks(path, lines, violations)
    return set(r_ids)


def validate_standard(spec_dir, violations):
    r_ids = set()
    missing = [f for f in STANDARD_FILES if not (spec_dir / f).exists()]
    if missing:
        violations.append(Violation(spec_dir, f"standard/full spec is missing {missing} (HUMAN_SPECS.md § Standard and full specs)"))
    req = spec_dir / "requirements.md"
    if req.exists():
        lines = req.read_text(encoding="utf-8").splitlines()
        check_when_owner(req, lines, violations)
        text = "\n".join(lines).lower()
        if "out of scope" not in text:
            violations.append(Violation(req, "requirements must list what is out of scope"))
        if "boundary" not in text:
            violations.append(Violation(req, "requirements must state the boundary — which modules change and which do not"))
        ids = check_ids(lines, "R")
        if not ids:
            violations.append(Violation(req, "no requirements — expected '- [ ] R<n>: ...' lines"))
        r_ids = set(ids)
        common_prose_checks(req, lines, violations)
    for f in ("design.md", "tasks.md"):
        if (spec_dir / f).exists():
            common_prose_checks(spec_dir / f, (spec_dir / f).read_text(encoding="utf-8").splitlines(), violations)
    return r_ids


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

    micro, quick = spec_dir / "micro-spec.md", spec_dir / "quick-spec.md"
    standard = any((spec_dir / f).exists() for f in STANDARD_FILES)
    present = [n for n, ok in (("micro-spec.md", micro.exists()), ("quick-spec.md", quick.exists()), ("requirements.md/design.md/tasks.md", standard)) if ok]
    if not present:
        violations.append(Violation(spec_dir, "no spec file — expected micro-spec.md, quick-spec.md, or requirements.md + design.md + tasks.md"))
        return violations
    if len(present) > 1:
        violations.append(Violation(spec_dir, f"more than one tier present: {present}"))
    if micro.exists():
        r_ids = validate_micro(micro, violations)
    elif quick.exists():
        r_ids = validate_quick(quick, violations)
    else:
        r_ids = validate_standard(spec_dir, violations)

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
