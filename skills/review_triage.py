#!/usr/bin/env python3
"""review_triage.py — mechanized review-claim triage per ~/agents/CODER.md §5 and ~/agents/review/ISSUE_TRACKING.md.

All review-store writes during triage go through this script. It enforces:
  - full IDs (<prefix><n>.<SID>, 22-char base62 UUID SID) — no bare short IDs
  - the gate ORDER: open → gate (cascade/scope/steering/creep/docs) → redlight → close
  - required evidence per state (scope:, cascade-of:, redlight:, probe output)
  - agent-allowed transitions only (DEFERRED / WILL_NOT_FIX are human-only and refused)
  - META open: / SUMMARY checkbox / detail status: kept in sync, log.md appended

Judgment stays with the agent (is it in scope? is it a cascade?) — the script only
accepts a decision WITH its evidence and records it correctly, or refuses.

Usage: review_triage.py --dir ~/reviews/<repo>-pr-<n> [--repo <checkout>] <command> ...

Commands:
  init      --repo-name R --pr N --branch B --base BASE --head SHA
  open      --type B|SEC|I|S|O|D|T|M --sev CRITICAL|HIGH|MEDIUM|LOW --title T --file 'path:line'
            --desc D --evidence E --fix F --reverify V        -> prints new full ID, warns on overlaps
  cascade-scan ID                                             -> prior issues overlapping this claim's files
  gate      ID (--pass | --docs-nit |
                --cascade-of FULLID --why W |
                --out-of-scope micro-spec|steering|scope-creep --why W)
  trace     ID (--possible --path P | --impossible --evidence E | --already-fixed SHA --evidence E)
            -> verdict from reading CURRENT HEAD code; red-light is refused until trace:possible.
               impossible/already-fixed do NOT close the claim — a committed green disproof test does.
  disprove  ID --sha SHA --test 'file:case' [--output O]      -> committed GREEN test disproving the claim; closes it
  redlight  ID --sha SHA --test 'file:case' [--output O]      -> records committed red proof
  unproven  ID --probe P --output O                           -> UNPROVEN with probe evidence
  needs-review ID --why W                                     -> NEEDS_REVIEW:coder pushback
  close     ID --fix-sha SHA --verify V                       -> CLOSED verified (needs triage pass + redlight)
  reopen    ID --why W
  list      [--all] [--tests]                                  -> --tests pairs each claim with its red-light test
  check                                                       -> store consistency lint (exit 1 on violation)
"""

import argparse
import datetime
import os
import re
import subprocess
import sys
import uuid

# KEEP-IN-SYNC: ~/agents/bin/sid.py is the master SID encoder.
ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


def new_sid():
    n = uuid.uuid4().int
    return "".join(ALPHABET[(n // 62**i) % 62] for i in range(21, -1, -1))


PREFIXES = ["B", "SEC", "I", "S", "O", "D", "T", "M"]
SEVERITIES = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
ID_RE = re.compile(r"^(B|SEC|I|S|O|D|T|M)(\d+)\.([0-9A-Za-z]{22})$")
NOT_CLOSED = ("OPEN", "NEEDS_REVIEW:reviewer", "NEEDS_REVIEW:coder", "NEEDS_REVIEW:cascade", "DEFERRED", "UNPROVEN")
HUMAN_ONLY = ("DEFERRED", "WILL_NOT_FIX")
WARNING = "** WARNING do not delete review entries ever **"


def die(msg, code=2):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


def today():
    return datetime.datetime.now().strftime("%Y-%m-%d")


class Store:
    def __init__(self, directory):
        self.dir = os.path.abspath(directory)
        self.review = os.path.join(self.dir, "review.md")
        self.log = os.path.join(self.dir, "log.md")

    # ---------- parsing ----------

    def exists(self):
        return os.path.isfile(self.review)

    def read(self):
        with open(self.review) as fh:
            return fh.read()

    def meta(self):
        m = {}
        for line in self.read().splitlines():
            if line.startswith("# SUMMARY"):
                break
            kv = re.match(r"^([a-z]+):(.*)$", line)
            if kv:
                m[kv.group(1)] = kv.group(2)
        return m

    def summary_items(self):
        items = {}
        in_summary = False
        for line in self.read().splitlines():
            if line.startswith("# SUMMARY"):
                in_summary = True
                continue
            if in_summary and line.startswith("- ") and line != "- none":
                m = re.match(r"^- \[( |x)\] (\S+) - (.+?) \[(\w+)\] - (.*)$", line)
                if m:
                    items[m.group(2)] = {
                        "checked": m.group(1) == "x",
                        "status": m.group(3),
                        "severity": m.group(4),
                        "title": m.group(5),
                    }
        return items

    def detail_path(self, full_id):
        return os.path.join(self.dir, f"{full_id}.md")

    def detail(self, full_id):
        p = self.detail_path(full_id)
        if not os.path.isfile(p):
            die(f"no detail file for {full_id} ({p})")
        with open(p) as fh:
            return fh.read()

    def detail_field(self, full_id, key):
        m = re.search(rf"^{key}:(.*)$", self.detail(full_id), re.M)
        return m.group(1).strip() if m else None

    # ---------- writing ----------

    def rewrite_summary(self, items):
        """Regenerate the SUMMARY list (sorted, no entry ever dropped) and the META open: line."""
        text = self.read()
        open_ids = [i for i, v in items.items() if v["status"] in NOT_CLOSED or v["status"].startswith("NEEDS_REVIEW")]
        open_line = "open:" + (",".join(sorted(open_ids, key=self._sort_key)) if open_ids else "none")
        text = re.sub(r"^open:.*$", open_line.replace("\\", "\\\\"), text, count=1, flags=re.M)
        text = re.sub(r"^reviewed:.*$", f"reviewed:{now()}", text, count=1, flags=re.M)

        lines = []
        for fid in sorted(items, key=self._sort_key):
            v = items[fid]
            box = "x" if v["checked"] else " "
            lines.append(f"- [{box}] {fid} - {v['status']} [{v['severity']}] - {v['title']}")
        block = "\n".join(lines) if lines else "- none"
        head, _, _ = text.partition("# SUMMARY")
        text = head + "# SUMMARY\n" + block + "\n"
        with open(self.review, "w") as fh:
            fh.write(text)

    @staticmethod
    def _sort_key(fid):
        m = ID_RE.match(fid)
        return (PREFIXES.index(m.group(1)), int(m.group(2))) if m else (99, 0)

    def set_status(self, full_id, status, checked, extra_lines=None):
        items = self.summary_items()
        if full_id not in items:
            die(f"{full_id} not in SUMMARY")
        items[full_id]["status"] = status
        items[full_id]["checked"] = checked
        self.rewrite_summary(items)
        detail = self.detail(full_id)
        detail = re.sub(r"^status:.*$", f"status:{status}", detail, count=1, flags=re.M)
        if extra_lines:
            detail = detail.rstrip("\n") + "\n" + "\n".join(extra_lines) + "\n"
        with open(self.detail_path(full_id), "w") as fh:
            fh.write(detail)

    def set_detail_field(self, full_id, key, value):
        detail = self.detail(full_id)
        if re.search(rf"^{key}:", detail, re.M):
            detail = re.sub(rf"^{key}:.*$", f"{key}:{value}", detail, count=1, flags=re.M)
        else:
            detail = detail.rstrip("\n") + f"\n{key}:{value}\n"
        with open(self.detail_path(full_id), "w") as fh:
            fh.write(detail)

    def append_log(self, full_id, status, file_ref, msg, head="-"):
        with open(self.log, "a") as fh:
            fh.write(f"{now()} - {head} - {full_id}:{status} - {file_ref} - {msg}\n")


# ---------- guards ----------

def require_id(s):
    if not ID_RE.match(s):
        die(f"'{s}' is not a full ID (<prefix><n>.<22-char SID>). Bare short IDs are not accepted — see REVIEW_METHOD.md § ID format.")
    return s


def require_triage_done(store, fid, for_what):
    t = store.detail_field(fid, "triage")
    if t not in ("passed", "passed-docs"):
        die(f"cannot {for_what} {fid}: triage is '{t or 'pending'}'. Run the gate command first — gates run in order, no skipping.", 1)
    return t


# ---------- commands ----------

def cmd_init(store, args):
    os.makedirs(store.dir, exist_ok=True)
    for f in ("feedback.md", "log.md"):
        p = os.path.join(store.dir, f)
        if not os.path.exists(p):
            open(p, "a").close()
    if store.exists():
        text = store.read()
        text = re.sub(r"^head:.*$", f"head:{args.head}", text, count=1, flags=re.M)
        text = re.sub(r"^reviewed:.*$", f"reviewed:{now()}", text, count=1, flags=re.M)
        with open(store.review, "w") as fh:
            fh.write(text)
        print(f"refreshed {store.review} (head, reviewed)")
        return
    with open(store.review, "w") as fh:
        fh.write(
            f"{WARNING}\n\n# META\nrepo:{args.repo_name}\npr:{args.pr}\nbranch:{args.branch}\n"
            f"base:{args.base}\nhead:{args.head}\nreviewed:{now()}\nopen:none\n\n# SUMMARY\n- none\n"
        )
    print(f"created {store.review}")


def overlap_scan(store, files):
    """Prior issues whose file: or commit-touched paths overlap the given paths."""
    hits = []
    basenames = {os.path.basename(f.split(":")[0]) for f in files if f}
    for fname in sorted(os.listdir(store.dir)):
        m = re.match(r"^(.+)\.md$", fname)
        if not m or fname in ("review.md", "feedback.md", "log.md") or not ID_RE.match(m.group(1)):
            continue
        fid = m.group(1)
        detail = store.detail(fid)
        for b in basenames:
            if b and b in detail:
                status = store.detail_field(fid, "status") or "?"
                hits.append((fid, status, b))
                break
    return hits


def cmd_open(store, args):
    if args.type not in PREFIXES:
        die(f"--type must be one of {PREFIXES}")
    if args.sev not in SEVERITIES:
        die(f"--sev must be one of {SEVERITIES}")
    items = store.summary_items()
    nums = [int(ID_RE.match(i).group(2)) for i in items if ID_RE.match(i) and ID_RE.match(i).group(1) == args.type]
    fid = f"{args.type}{max(nums) + 1 if nums else 1}.{new_sid()}"
    meta = store.meta()
    with open(store.detail_path(fid), "w") as fh:
        fh.write(
            f"## {fid}\nID:{fid}\ntype:{args.type}\nseverity:{args.sev}\ntitle:{args.title}\n"
            f"file:`{args.file}`\npr:`#{meta.get('pr', '?')}`\nstatus:OPEN\ntriage:pending\ntrace:pending\nredlight:pending\n\n"
            f"description:\n{args.desc}\n\nevidence:\n```evidence\n{args.evidence}\n```\n\n"
            f"fix:{args.fix}\nreverify:{args.reverify}\n"
        )
    items[fid] = {"checked": False, "status": "OPEN", "severity": args.sev, "title": f"{args.title} `{args.file}`"}
    store.rewrite_summary(items)
    store.append_log(fid, "OPEN", args.file, "claim recorded (unproven, triage pending)", meta.get("head", "-"))
    print(fid)
    hits = overlap_scan(store, [args.file])
    for hid, status, path in hits:
        if hid != fid:
            print(f"POSSIBLE CASCADE: overlaps {hid} ({status}) on '{path}' — run cascade-scan / gate before anything else", file=sys.stderr)


def cmd_cascade_scan(store, args):
    fid = require_id(args.id)
    file_ref = (store.detail_field(fid, "file") or "").strip("`")
    hits = [(h, s, p) for h, s, p in overlap_scan(store, [file_ref]) if h != fid]
    if not hits:
        print("no overlapping prior issues found")
        return
    for hid, status, path in hits:
        print(f"{hid} - {status} - overlaps on '{path}'")


def cmd_gate(store, args):
    fid = require_id(args.id)
    status = store.detail_field(fid, "status")
    if status != "OPEN":
        die(f"gate applies to OPEN claims; {fid} is {status}", 1)
    if args.cascade_of:
        require_id(args.cascade_of)
        if not args.why:
            die("--cascade-of requires --why explaining how the prior fix led to this claim")
        store.set_status(fid, "NEEDS_REVIEW:cascade", False,
                         [f"cascade-of:{args.cascade_of}", f"cascade-why:{args.why}"])
        store.set_detail_field(fid, "triage", "gated-cascade")
        store.append_log(fid, "NEEDS_REVIEW:cascade", "-", f"cascade of {args.cascade_of}; awaiting user ruling")
        print(f"{fid} -> NEEDS_REVIEW:cascade (cascade-of:{args.cascade_of}). Do NOT fix without user approval.")
    elif args.out_of_scope:
        if args.out_of_scope not in ("micro-spec", "steering", "scope-creep"):
            die("--out-of-scope must be micro-spec|steering|scope-creep")
        if not args.why:
            die("--out-of-scope requires --why")
        store.set_status(fid, "OUT_OF_SCOPE", True, [f"scope:{args.out_of_scope} - {args.why}"])
        store.set_detail_field(fid, "triage", "gated-scope")
        store.append_log(fid, "OUT_OF_SCOPE", "-", f"{args.out_of_scope}: {args.why}")
        print(f"{fid} -> OUT_OF_SCOPE ({args.out_of_scope})")
    elif args.docs_nit:
        store.set_detail_field(fid, "triage", "passed-docs")
        store.set_detail_field(fid, "redlight", "n/a-docs")
        store.append_log(fid, "OPEN", "-", "triage passed as docs-nit; fix must not change micro-spec/steering design")
        print(f"{fid} triage:passed-docs — doc fix allowed only if it does not change the design")
    elif args.passed:
        store.set_detail_field(fid, "triage", "passed")
        store.append_log(fid, "OPEN", "-", "triage passed (cascade/micro-spec/steering/creep all clear)")
        print(f"{fid} triage:passed — proceed to red-light")
    else:
        die("gate needs one of --pass / --docs-nit / --cascade-of / --out-of-scope")


def cmd_trace(store, args, repo):
    fid = require_id(args.id)
    t = require_triage_done(store, fid, "trace")
    if t == "passed-docs":
        die("docs-nit claims do not need a trace", 1)
    picked = [x for x in (args.possible, args.impossible, bool(args.already_fixed)) if x]
    if len(picked) != 1:
        die("trace needs exactly one of --possible / --impossible / --already-fixed SHA")
    if args.possible:
        if not args.path:
            die("--possible requires --path: the current-HEAD file:line trace of how the defect manifests")
        store.set_detail_field(fid, "trace", "possible")
        store.set_status(fid, "OPEN", False, ["trace-evidence:", "```evidence", args.path, "```"])
        store.append_log(fid, "OPEN", "-", "trace: defect possible on current HEAD")
        print(f"{fid} trace:possible — proceed to red-light")
    elif args.impossible:
        if not args.evidence:
            die("--impossible requires --evidence: current-HEAD file:line quotes (types, guards, constraints) showing the defect cannot manifest")
        store.set_detail_field(fid, "trace", "impossible")
        store.set_status(fid, "OPEN", False, ["trace-evidence:", "```evidence", args.evidence, "```"])
        store.append_log(fid, "OPEN", "-", "trace: defect impossible on current HEAD; green disproof test required")
        print(f"{fid} trace:impossible — commit a GREEN disproof test and record it with `disprove` (use `unproven` only if no test is constructable)")
    else:
        sha = args.already_fixed
        if not re.match(r"^[0-9a-f]{7,40}$", sha):
            die("--already-fixed must be a commit sha")
        if not args.evidence:
            die("--already-fixed requires --evidence: current-HEAD file:line quotes showing the fix in place")
        if repo:
            r = subprocess.run(["git", "-C", repo, "merge-base", "--is-ancestor", sha, "HEAD"], capture_output=True)
            if r.returncode != 0:
                die(f"{sha} is not an ancestor of HEAD in {repo} — an 'already fixed' claim needs the fix commit on this branch", 1)
        store.set_detail_field(fid, "trace", f"already-fixed {sha}")
        store.set_status(fid, "OPEN", False, [f"fixed-by:{sha}", "trace-evidence:", "```evidence", args.evidence, "```"])
        store.append_log(fid, "OPEN", "-", f"trace: already fixed by {sha}; green regression test required to close")
        print(f"{fid} trace:already-fixed {sha} — commit the GREEN regression/disproof test and record it with `disprove` to close")


def cmd_disprove(store, args, repo):
    fid = require_id(args.id)
    tr = store.detail_field(fid, "trace") or "pending"
    if tr != "impossible" and not tr.startswith("already-fixed"):
        die(f"disprove applies only after a trace verdict of impossible/already-fixed; {fid} trace is '{tr}'", 1)
    if not re.match(r"^[0-9a-f]{7,40}$", args.sha):
        die("--sha must be the commit sha of the committed green disproof test")
    if repo:
        r = subprocess.run(["git", "-C", repo, "cat-file", "-t", args.sha], capture_output=True, text=True)
        if r.stdout.strip() != "commit":
            die(f"sha {args.sha} not found in {repo} — the disproof test must be COMMITTED", 1)
        test_file = args.test.split(":")[0]
        r = subprocess.run(["git", "-C", repo, "show", "--name-only", "--format=", args.sha], capture_output=True, text=True)
        if test_file not in r.stdout:
            die(f"commit {args.sha} does not touch {test_file} — wrong sha or uncommitted test", 1)
    store.set_detail_field(fid, "redlight", f"disproof {args.sha} {args.test}")
    fixed_by = store.detail_field(fid, "fixed-by")
    note = f"already fixed by {fixed_by}; " if fixed_by else ""
    store.set_status(fid, f"CLOSED verified:{today()}", True,
                     [f"commit:`{fixed_by or args.sha}`", "disproof-output:", "```evidence", args.output or "(green)", "```",
                      f"fixed:{note}claim disproven by green test {args.test}"])
    store.append_log(fid, f"CLOSED verified:{today()}", args.test, f"{note}disproven by green test at {args.sha}")
    print(f"{fid} -> CLOSED verified:{today()} — {note}disproven by green test {args.test} ({args.sha})")


def cmd_redlight(store, args, repo):
    fid = require_id(args.id)
    require_triage_done(store, fid, "red-light")
    tr = store.detail_field(fid, "trace") or "pending"
    if tr != "possible":
        die(f"cannot red-light {fid}: trace is '{tr}'. Trace the claim against current HEAD first — the claim's own text is not evidence about the code.", 1)
    if not re.match(r"^[0-9a-f]{7,40}$", args.sha):
        die("--sha must be a commit sha")
    if repo:
        r = subprocess.run(["git", "-C", repo, "cat-file", "-t", args.sha], capture_output=True, text=True)
        if r.stdout.strip() != "commit":
            die(f"sha {args.sha} not found in {repo} — the red test must be COMMITTED (CODER.md: committed red)", 1)
        test_file = args.test.split(":")[0]
        r = subprocess.run(["git", "-C", repo, "show", "--name-only", "--format=", args.sha], capture_output=True, text=True)
        if test_file not in r.stdout:
            die(f"commit {args.sha} does not touch {test_file} — wrong sha or uncommitted test", 1)
    store.set_detail_field(fid, "redlight", f"{args.sha} {args.test}")
    if args.output:
        store.set_status(fid, "OPEN", False, ["red-output:", "```evidence", args.output, "```"])
    store.append_log(fid, "OPEN", args.test, f"red-lighted at {args.sha}")
    print(f"{fid} red-lighted: {args.sha} {args.test} — proceed to fix (never edit the test to pass)")


def cmd_unproven(store, args):
    fid = require_id(args.id)
    require_triage_done(store, fid, "mark unproven")
    if not args.probe or not args.output:
        die("unproven requires --probe (test code/path) and --output (its passing output)")
    store.set_status(fid, "UNPROVEN", False,
                     ["probe:", "```evidence", args.probe, "```", "probe-output:", "```evidence", args.output, "```"])
    store.append_log(fid, "UNPROVEN", "-", "could not red-light; awaiting human decision")
    print(f"{fid} -> UNPROVEN (stays open for user decision; no fix)")


def cmd_needs_review(store, args):
    fid = require_id(args.id)
    if not args.why:
        die("needs-review requires --why with evidence")
    store.set_status(fid, "NEEDS_REVIEW:coder", False, [f"pushback:{today()} - {args.why}"])
    store.append_log(fid, "NEEDS_REVIEW:coder", "-", args.why)
    print(f"{fid} -> NEEDS_REVIEW:coder")


def cmd_close(store, args, repo):
    fid = require_id(args.id)
    triage = require_triage_done(store, fid, "close")
    red = store.detail_field(fid, "redlight") or "pending"
    if red == "pending":
        die(f"cannot close {fid}: no red-light recorded. A claim with no committed red test cannot be CLOSED (CODER.md §5).", 1)
    if triage == "passed" and red == "n/a-docs":
        die(f"cannot close {fid}: redlight:n/a-docs is only valid for docs-nit triage", 1)
    if not re.match(r"^[0-9a-f]{7,40}$", args.fix_sha):
        die("--fix-sha must be a commit sha")
    if repo:
        r = subprocess.run(["git", "-C", repo, "cat-file", "-t", args.fix_sha], capture_output=True, text=True)
        if r.stdout.strip() != "commit":
            die(f"fix sha {args.fix_sha} not found in {repo}", 1)
    store.set_status(fid, f"CLOSED verified:{today()}", True,
                     [f"commit:`{args.fix_sha}`", f"fixed:{args.verify}"])
    store.append_log(fid, f"CLOSED verified:{today()}", "-", f"fix {args.fix_sha}; proven by {red}; {args.verify}")
    proof = "docs-only change (no test applicable)" if red == "n/a-docs" else f"proven by test {red}"
    print(f"{fid} -> CLOSED verified:{today()} — fix {args.fix_sha}; {proof}")


def cmd_reopen(store, args):
    fid = require_id(args.id)
    store.set_status(fid, "OPEN", False, [f"reopened:{today()} - {args.why or 'no reason given'}"])
    store.append_log(fid, "OPEN", "-", f"reopened: {args.why}")
    print(f"{fid} -> OPEN")


def cmd_list(store, args):
    for fid, v in sorted(store.summary_items().items(), key=lambda kv: Store._sort_key(kv[0])):
        if args.all or not v["checked"]:
            box = "x" if v["checked"] else " "
            print(f"- [{box}] {fid} - {v['status']} [{v['severity']}] - {v['title']}")
            if args.tests:
                red = store.detail_field(fid, "redlight") or "pending"
                print(f"      test: {red}")


def cmd_check(store, args):
    problems = []
    meta = store.meta()
    items = store.summary_items()
    open_ids = [] if meta.get("open") in (None, "none") else meta["open"].split(",")
    for fid in open_ids:
        if fid not in items:
            problems.append(f"open: lists {fid} but SUMMARY has no item")
    for fid, v in items.items():
        if not ID_RE.match(fid):
            problems.append(f"{fid}: not a full ID (missing SID)")
            continue
        if not os.path.isfile(store.detail_path(fid)):
            problems.append(f"{fid}: SUMMARY item has no detail file")
            continue
        ds = store.detail_field(fid, "status")
        if ds != v["status"]:
            problems.append(f"{fid}: SUMMARY says '{v['status']}' but detail says '{ds}'")
        not_closed = v["status"] in NOT_CLOSED
        if not_closed and v["checked"]:
            problems.append(f"{fid}: not-closed status but checkbox is [x]")
        if not not_closed and not v["checked"]:
            problems.append(f"{fid}: closed status but checkbox is [ ]")
        if not_closed and fid not in open_ids:
            problems.append(f"{fid}: not-closed but missing from META open:")
        if not not_closed and fid in open_ids:
            problems.append(f"{fid}: closed but still in META open:")
        if v["status"] == "NEEDS_REVIEW:cascade" and not store.detail_field(fid, "cascade-of"):
            problems.append(f"{fid}: NEEDS_REVIEW:cascade without cascade-of:")
        if v["status"] == "OUT_OF_SCOPE" and not store.detail_field(fid, "scope"):
            problems.append(f"{fid}: OUT_OF_SCOPE without scope:")
        if v["status"].startswith("CLOSED") and (store.detail_field(fid, "redlight") or "pending") == "pending":
            problems.append(f"{fid}: CLOSED without a redlight record")
    if problems:
        print("\n".join(f"FAIL: {p}" for p in problems))
        sys.exit(1)
    print(f"store consistent ({len(items)} issues, {len(open_ids)} not-closed)")


def main():
    ap = argparse.ArgumentParser(description="Mechanized review-claim triage store operations.")
    ap.add_argument("--dir", required=True, help="review directory ~/reviews/<repo>-pr-<n>")
    ap.add_argument("--repo", default=None, help="repo checkout for sha verification")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init")
    p.add_argument("--repo-name", required=True)
    p.add_argument("--pr", required=True)
    p.add_argument("--branch", required=True)
    p.add_argument("--base", required=True)
    p.add_argument("--head", required=True)

    p = sub.add_parser("open")
    for opt in ("--type", "--sev", "--title", "--file", "--desc", "--evidence", "--fix", "--reverify"):
        p.add_argument(opt, required=True)

    p = sub.add_parser("cascade-scan")
    p.add_argument("id")

    p = sub.add_parser("gate")
    p.add_argument("id")
    p.add_argument("--pass", dest="passed", action="store_true")
    p.add_argument("--docs-nit", action="store_true")
    p.add_argument("--cascade-of", default=None)
    p.add_argument("--out-of-scope", default=None)
    p.add_argument("--why", default=None)

    p = sub.add_parser("trace")
    p.add_argument("id")
    p.add_argument("--possible", action="store_true")
    p.add_argument("--impossible", action="store_true")
    p.add_argument("--already-fixed", default=None, metavar="SHA")
    p.add_argument("--path", default=None)
    p.add_argument("--evidence", default=None)

    p = sub.add_parser("redlight")
    p.add_argument("id")
    p.add_argument("--sha", required=True)
    p.add_argument("--test", required=True)
    p.add_argument("--output", default=None)

    p = sub.add_parser("disprove")
    p.add_argument("id")
    p.add_argument("--sha", required=True)
    p.add_argument("--test", required=True)
    p.add_argument("--output", default=None)

    p = sub.add_parser("unproven")
    p.add_argument("id")
    p.add_argument("--probe", required=True)
    p.add_argument("--output", required=True)

    p = sub.add_parser("needs-review")
    p.add_argument("id")
    p.add_argument("--why", required=True)

    p = sub.add_parser("close")
    p.add_argument("id")
    p.add_argument("--fix-sha", required=True)
    p.add_argument("--verify", required=True)

    p = sub.add_parser("reopen")
    p.add_argument("id")
    p.add_argument("--why", required=True)

    p = sub.add_parser("list")
    p.add_argument("--all", action="store_true")
    p.add_argument("--tests", action="store_true", help="show each claim's matching red-light test")

    sub.add_parser("check")

    args = ap.parse_args()
    store = Store(args.dir)
    if args.cmd != "init" and not store.exists():
        die(f"no review store at {store.review} — run init first")

    if args.cmd == "init":
        cmd_init(store, args)
    elif args.cmd == "open":
        cmd_open(store, args)
    elif args.cmd == "cascade-scan":
        cmd_cascade_scan(store, args)
    elif args.cmd == "gate":
        cmd_gate(store, args)
    elif args.cmd == "trace":
        cmd_trace(store, args, args.repo)
    elif args.cmd == "redlight":
        cmd_redlight(store, args, args.repo)
    elif args.cmd == "disprove":
        cmd_disprove(store, args, args.repo)
    elif args.cmd == "unproven":
        cmd_unproven(store, args)
    elif args.cmd == "needs-review":
        cmd_needs_review(store, args)
    elif args.cmd == "close":
        cmd_close(store, args, args.repo)
    elif args.cmd == "reopen":
        cmd_reopen(store, args)
    elif args.cmd == "list":
        cmd_list(store, args)
    elif args.cmd == "check":
        cmd_check(store, args)


if __name__ == "__main__":
    main()
