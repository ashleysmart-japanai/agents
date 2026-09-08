#!/usr/bin/env python3
"""Validate a spec directory against design/SPECS.md.

Checks the human tier file (microspec.md, quick-spec.md, standard-spec.md, full-spec.md)
and, when present, the agent's agent_tasking.md beside it.

Usage:
    python3 validate_spec.py <spec-dir> [<spec-dir> ...]
    python3 validate_spec.py <project>/docs/20260908_my-task/microspec.md   # file path also accepted

Exit codes:
    0 = all checks passed
    1 = violations found
"""

import re
import sys
import argparse
from pathlib import Path

TIER_FILES = {
    "microspec.md": "micro",
    "quick-spec.md": "quick",
    "standard-spec.md": "standard",
    "full-spec.md": "full",
}
TASKING_FILE = "agent_tasking.md"

# Section keywords matched against normalized headings (numbering and parentheticals stripped, lowercased).
REQUIRED_SECTIONS = {
    "micro": ["goal", "scope", "behaviour", "error cases", "alternatives", "open questions"],
    "quick": ["goal", "scope", "behaviour", "error cases", "alternatives", "open questions", "design", "use cases"],
    "standard": ["requirements", "design", "use cases", "acceptance checklist", "references"],
    "full": ["requirements", "design", "use cases", "acceptance checklist", "references"],
}
# Agent-authored sections never appear in a human spec.
AGENT_SECTIONS = ["task breakdown", "test plan", "security checklist"]
# Human-authored sections never appear in the tasking file.
HUMAN_ONLY_SECTIONS = ["requirements", "acceptance checklist"]
TASKING_REQUIRED = ["task breakdown", "test plan", "security checklist"]

HEADER_KEYS = ("What", "When", "Owner")
DEFAULT_S = [f"S{i}" for i in range(1, 11)]
DEFAULT_X = [f"X{i}" for i in range(1, 7)]

HEADING_RE = re.compile(r"^(#{1,3})\s+(.*\S)\s*$")
CHECK_ID_RE = re.compile(r"^- \[[ x]\] ([RUAXS])(\d+):")
TRACKER_RE = re.compile(r"\bDONE\b|\bStatus:|\bREVERTED\b|NOT IMPLEMENTED|at spec phase")
LINE_NUMBER_REF_RE = re.compile(r"\b[\w./-]+\.[A-Za-z]{1,5}:\d+\b")
DIR_NAME_RE = re.compile(r"^(\d{8}_)?[a-z0-9][a-z0-9-]*$")


class Violation:
    def __init__(self, path, message):
        self.path = path
        self.message = message

    def __str__(self):
        return f"  FAIL  {self.path}: {self.message}"


def normalize_heading(text):
    text = re.sub(r"^\d+\.\s*", "", text)
    text = re.sub(r"\s*\(.*?\)\s*", " ", text)
    text = text.replace("behavior", "behaviour")
    return " ".join(text.lower().split())


def parse_sections(lines):
    """Return list of (normalized heading, level, [body lines])."""
    sections = []
    preamble = []
    current = None
    for line in lines:
        m = HEADING_RE.match(line)
        if m and len(m.group(1)) >= 2:
            current = (normalize_heading(m.group(2)), len(m.group(1)), [])
            sections.append(current)
        elif current is None:
            preamble.append(line)
        else:
            current[2].append(line)
    return preamble, sections


def has_section(sections, keyword):
    return any(keyword in name for name, _, _ in sections)


def section_body(sections, keyword):
    body = []
    for name, _, lines in sections:
        if keyword in name:
            body.extend(lines)
    return body


def check_ids(lines, prefix):
    ids = []
    for l in lines:
        m = CHECK_ID_RE.match(l)
        if m and m.group(1) == prefix:
            ids.append(int(m.group(2)))
    return ids


def common_prose_checks(path, lines, violations):
    for i, l in enumerate(lines, 1):
        if l.lstrip().startswith("```"):
            continue
        if TRACKER_RE.search(l):
            violations.append(Violation(path, f"line {i}: tracker marker in spec prose (SPECS.md § The spec is not a tracker)"))
        if LINE_NUMBER_REF_RE.search(l):
            violations.append(Violation(path, f"line {i}: line-number citation — use durable references (SPECS.md § Objective)"))


def validate_tier_file(path, tier, violations):
    lines = path.read_text(encoding="utf-8").splitlines()
    preamble, sections = parse_sections(lines)

    # Three questions in the header, before the first section.
    for key in HEADER_KEYS:
        hits = [l for l in preamble if re.match(rf"^- {key}: \S", l)]
        if len(hits) != 1:
            violations.append(Violation(path, f"header must answer '- {key}: <text>' exactly once before the first section (found {len(hits)})"))

    for kw in REQUIRED_SECTIONS[tier]:
        if not has_section(sections, kw):
            violations.append(Violation(path, f"{tier} spec is missing section '{kw}' (SPECS.md § Tier shapes)"))
    for kw in AGENT_SECTIONS:
        if has_section(sections, kw):
            violations.append(Violation(path, f"section '{kw}' is agent-authored and belongs in {TASKING_FILE}, not the spec"))
    if tier == "micro" and has_section(sections, "design"):
        violations.append(Violation(path, "micro spec has a Design section — the fix is the design (SPECS.md § Tier shapes)"))

    # Scope: out of scope + boundary.
    if tier in ("micro", "quick"):
        scope = section_body(sections, "scope")
        if not any("out of scope" in l.lower() for l in scope):
            violations.append(Violation(path, "Scope must list what is out of scope"))
        if not any("boundary" in l.lower() for l in scope):
            violations.append(Violation(path, "Scope must state the boundary — which modules change and which do not"))
    else:
        req = section_body(sections, "requirements")
        if not any("out of scope" in l.lower() for l in req):
            violations.append(Violation(path, "Requirements must list what is out of scope"))
        if not any("boundary" in l.lower() for l in req):
            violations.append(Violation(path, "Requirements must state the boundary — which modules change and which do not"))

    # R ids: at least one, unique.
    r_ids = check_ids(lines, "R")
    if not r_ids:
        violations.append(Violation(path, "no acceptance criteria — expected '- [ ] R<n>: ...' lines"))
    elif len(r_ids) != len(set(r_ids)):
        violations.append(Violation(path, f"duplicate R ids: {sorted(set(i for i in r_ids if r_ids.count(i) > 1))}"))

    if tier in ("quick", "standard", "full") and not check_ids(lines, "U"):
        violations.append(Violation(path, "no use cases — expected '- [ ] U<n>: ...' lines"))
    if tier in ("standard", "full"):
        present = {f"X{i}" for i in check_ids(lines, "X")}
        missing = [x for x in DEFAULT_X if x not in present]
        if missing:
            violations.append(Violation(path, f"acceptance checklist missing default items: {missing}"))

    common_prose_checks(path, lines, violations)
    return set(r_ids)


def validate_tasking_file(path, spec_r_ids, violations):
    lines = path.read_text(encoding="utf-8").splitlines()
    text = "\n".join(lines)
    _, sections = parse_sections(lines)

    for kw in TASKING_REQUIRED:
        if not has_section(sections, kw):
            violations.append(Violation(path, f"tasking file is missing section '{kw}' (SPECS.md § Tasking file)"))
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
    if spec_r_ids and not referenced:
        violations.append(Violation(path, "tasking file references no R<id> from the spec"))
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
        violations.append(Violation(spec_dir, "directory name must be <YYYYMMDD>_<slug> or <module-slug> (lowercase, digits, hyphens)"))

    tiers = [(f, t) for f, t in TIER_FILES.items() if (spec_dir / f).exists()]
    if not tiers:
        violations.append(Violation(spec_dir, f"no tier file — expected one of {', '.join(TIER_FILES)}"))
        return violations
    if len(tiers) > 1:
        violations.append(Violation(spec_dir, f"more than one tier file: {[f for f, _ in tiers]}"))
    fname, tier = tiers[0]
    r_ids = validate_tier_file(spec_dir / fname, tier, violations)

    tasking = spec_dir / TASKING_FILE
    if tasking.exists():
        validate_tasking_file(tasking, r_ids, violations)
    return violations


def main():
    parser = argparse.ArgumentParser(description="Validate spec directories against design/SPECS.md")
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
