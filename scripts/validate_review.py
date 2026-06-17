#!/usr/bin/env python3
"""Validate review directories against ISSUE_TRACKING.md contract.

Designed to run on a crontab. Scans ~/reviews/ for all review directories,
checks each one for structural integrity, and reports violations.

Usage:
    python3 validate_review.py                  # check all reviews
    python3 validate_review.py ~/reviews/repo-pr-42/  # check one review
    python3 validate_review.py --since 30       # only reviews modified in last 30 min (default)
    python3 validate_review.py --since 0        # all reviews regardless of age

Exit codes:
    0 = all checks passed
    1 = violations found
"""

import os
import re
import sys
import time
import argparse
from pathlib import Path

REVIEWS_ROOT = Path.home() / "reviews"

# --- ID pattern: valid prefixes from ISSUE_TRACKING.md ---
VALID_PREFIXES = ("B", "SEC", "I", "S", "O", "D", "T", "M")
ID_RE = re.compile(r"^(?:B|SEC|I|S|O|D|T|M)\d+$")

# --- SUMMARY line grammar ---
# - [ ] B1 - OPEN [HIGH] - some text
# - [x] B2 - CLOSED verified:2026-06-11 [MEDIUM] - some text
SUMMARY_RE = re.compile(
    r"^- \[([ x])\] "
    r"((?:B|SEC|I|S|O|D|T|M)\d+) - "
    r"(OPEN|NEEDS_REVIEW:reviewer|NEEDS_REVIEW:coder|DEFERRED|CLOSED verified:\d{4}-\d{2}-\d{2}|WILL_NOT_FIX) "
    r"\[(CRITICAL|HIGH|MEDIUM|LOW)\] - "
    r"(.+)$"
)

# --- META required keys ---
META_REQUIRED = ("repo:", "pr:", "branch:", "base:", "head:", "reviewed:", "open:")

# --- Detail file required fields ---
DETAIL_REQUIRED = (
    "ID:", "type:", "severity:", "title:", "file:",
    "pr:", "status:", "description:", "evidence:", "fix:", "reverify:",
)

NOT_CLOSED_STATUSES = {"OPEN", "NEEDS_REVIEW:reviewer", "NEEDS_REVIEW:coder", "DEFERRED"}
CLOSED_STATUSES_PREFIX = ("CLOSED verified:", "WILL_NOT_FIX")


class Violation:
    def __init__(self, path, message):
        self.path = path
        self.message = message

    def __str__(self):
        return f"  FAIL  {self.path}: {self.message}"


def parse_review_md(review_path):
    """Parse review.md and return meta dict, summary entries, and raw lines."""
    text = review_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    meta = {}
    summary_entries = []
    current_section = None

    for line in lines:
        stripped = line.strip()
        if stripped == "# META":
            current_section = "meta"
            continue
        elif stripped == "# SUMMARY":
            current_section = "summary"
            continue
        elif stripped.startswith("# ") and current_section:
            current_section = None
            continue

        if current_section == "meta" and ":" in stripped:
            key, _, value = stripped.partition(":")
            meta[key.strip() + ":"] = value.strip()
        elif current_section == "summary" and stripped.startswith("- ["):
            summary_entries.append(stripped)

    return meta, summary_entries, lines


def validate_review_dir(review_dir):
    """Validate a single review directory. Returns list of Violations."""
    violations = []
    review_md = review_dir / "review.md"

    if not review_md.exists():
        violations.append(Violation(review_dir, "missing review.md"))
        return violations

    # --- Parse review.md ---
    meta, summary_entries, lines = parse_review_md(review_md)

    # --- Check warning line ---
    if not lines or "WARNING" not in lines[0]:
        violations.append(Violation(review_md, "missing WARNING line at top"))

    # --- Check META required keys ---
    for key in META_REQUIRED:
        if key not in meta:
            violations.append(Violation(review_md, f"META missing required key: {key}"))

    # --- Check no DETAILS section exists ---
    for line in lines:
        if line.strip() == "# DETAILS":
            violations.append(Violation(review_md, "contains # DETAILS section (should not exist)"))
            break

    # --- Check no inline detail records ---
    for i, line in enumerate(lines):
        if re.match(r"^## (B|SEC|I|S|O|D|T|M)\d+", line.strip()):
            violations.append(Violation(review_md, f"line {i+1}: inline detail record '{line.strip()}' (details must be in <ID>.md files)"))

    # --- Parse SUMMARY entries ---
    summary_ids = {}
    for entry in summary_entries:
        if entry.strip() == "- none":
            continue
        m = SUMMARY_RE.match(entry)
        if not m:
            violations.append(Violation(review_md, f"malformed SUMMARY entry: {entry}"))
            continue
        checkbox, issue_id, status, severity, text = m.groups()
        summary_ids[issue_id] = {
            "checkbox": checkbox,
            "status": status,
            "severity": severity,
            "text": text,
        }

    # --- Parse open: from META ---
    open_ids = set()
    open_raw = meta.get("open:", "")
    if open_raw and open_raw != "none":
        open_ids = {x.strip() for x in open_raw.split(",") if x.strip()}

    # --- Check open: consistency with SUMMARY ---
    for issue_id, info in summary_ids.items():
        is_closed = info["status"].startswith("CLOSED") or info["status"] == "WILL_NOT_FIX"
        in_open = issue_id in open_ids

        if is_closed and in_open:
            violations.append(Violation(review_md, f"{issue_id}: closed but listed in open:"))
        if not is_closed and not in_open:
            violations.append(Violation(review_md, f"{issue_id}: not-closed but missing from open:"))

        # checkbox alignment
        if is_closed and info["checkbox"] != "x":
            violations.append(Violation(review_md, f"{issue_id}: closed but checkbox is [ ]"))
        if not is_closed and info["checkbox"] != " ":
            violations.append(Violation(review_md, f"{issue_id}: not-closed but checkbox is [x]"))

    # orphan IDs in open: not in SUMMARY
    for oid in open_ids:
        if oid not in summary_ids:
            violations.append(Violation(review_md, f"open: lists {oid} but no SUMMARY entry"))

    # --- List <ID>.md files on disk ---
    detail_files = {}
    for f in review_dir.iterdir():
        if f.name in ("review.md", "feedback.md", "feedback.lock.md", "log.md"):
            continue
        if f.suffix == ".md" and f.is_file():
            stem = f.stem
            if ID_RE.match(stem):
                detail_files[stem] = f

    # --- Every SUMMARY entry must have an <ID>.md file ---
    for issue_id in summary_ids:
        if issue_id not in detail_files:
            violations.append(Violation(review_dir, f"{issue_id}: SUMMARY entry but no {issue_id}.md file"))

    # --- Every <ID>.md file should have a SUMMARY entry ---
    for file_id in detail_files:
        if file_id not in summary_ids:
            violations.append(Violation(review_dir, f"{file_id}.md exists but no SUMMARY entry"))

    # --- Validate each detail file ---
    for issue_id, detail_path in detail_files.items():
        detail_violations = validate_detail_file(detail_path, issue_id, summary_ids.get(issue_id))
        violations.extend(detail_violations)

    return violations


def validate_detail_file(detail_path, issue_id, summary_info):
    """Validate a single <ID>.md detail file."""
    violations = []
    try:
        text = detail_path.read_text(encoding="utf-8")
    except Exception as e:
        violations.append(Violation(detail_path, f"cannot read: {e}"))
        return violations

    lines = text.splitlines()

    # --- Check minimum content (not a stub) ---
    non_empty = [l for l in lines if l.strip()]
    if len(non_empty) < 10:
        violations.append(Violation(detail_path, f"too short ({len(non_empty)} non-empty lines, minimum 10) — likely a stub"))

    # --- Check required fields ---
    found_fields = set()
    for line in lines:
        stripped = line.strip()
        for field in DETAIL_REQUIRED:
            if stripped.startswith(field):
                found_fields.add(field)

    for field in DETAIL_REQUIRED:
        if field not in found_fields:
            violations.append(Violation(detail_path, f"missing required field: {field}"))

    # --- Check evidence has content ---
    in_evidence = False
    evidence_lines = 0
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("evidence:"):
            in_evidence = True
            continue
        if in_evidence:
            if stripped.startswith("fix:") or stripped.startswith("reverify:"):
                break
            if stripped and not stripped.startswith("```"):
                evidence_lines += 1
    if "evidence:" in found_fields and evidence_lines == 0:
        violations.append(Violation(detail_path, "evidence section is empty"))

    # --- Check description has content ---
    in_desc = False
    desc_lines = 0
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("description:"):
            in_desc = True
            continue
        if in_desc:
            if stripped.startswith("evidence:"):
                break
            if stripped:
                desc_lines += 1
    if "description:" in found_fields and desc_lines == 0:
        violations.append(Violation(detail_path, "description section is empty"))

    # --- Check status matches SUMMARY ---
    if summary_info:
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("status:"):
                detail_status = stripped[len("status:"):].strip()
                summary_status = summary_info["status"]
                if detail_status != summary_status:
                    violations.append(Violation(
                        detail_path,
                        f"status mismatch: file has '{detail_status}', SUMMARY has '{summary_status}'"
                    ))
                break

    return violations


def find_review_dirs(since_minutes):
    """Find review directories, optionally filtered by modification time."""
    if not REVIEWS_ROOT.exists():
        return []

    dirs = []
    now = time.time()
    cutoff = now - (since_minutes * 60) if since_minutes > 0 else 0

    for entry in REVIEWS_ROOT.iterdir():
        if not entry.is_dir():
            continue
        review_md = entry / "review.md"
        if not review_md.exists():
            continue
        if cutoff > 0:
            mtime = review_md.stat().st_mtime
            if mtime < cutoff:
                continue
        dirs.append(entry)

    return sorted(dirs)


def main():
    parser = argparse.ArgumentParser(description="Validate review directories")
    parser.add_argument("path", nargs="?", help="specific review directory to check")
    parser.add_argument("--since", type=int, default=30,
                        help="only check reviews modified in last N minutes (0 = all)")
    args = parser.parse_args()

    if args.path:
        dirs = [Path(args.path)]
    else:
        dirs = find_review_dirs(args.since)

    if not dirs:
        print("No review directories to check.")
        return 0

    total_violations = 0
    for review_dir in dirs:
        violations = validate_review_dir(review_dir)
        if violations:
            print(f"\n{review_dir.name}  ({len(violations)} violations)")
            for v in violations:
                print(str(v))
            total_violations += len(violations)
        else:
            print(f"{review_dir.name}  OK")

    print(f"\n{'='*60}")
    print(f"Checked {len(dirs)} review(s), {total_violations} violation(s)")

    return 1 if total_violations > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
