#!/usr/bin/env python3
"""RALPH Coder — watches a review file for changes and triggers a Claude cleanup pass."""

import hashlib
import os
import subprocess
import sys
import time

POLL_INTERVAL = 60
PROMPT_FILE = os.path.join(os.path.dirname(__file__), "RALPH_REVIEW_CLEANUP.md")


def run(cmd, *, check=True, capture=True):
    result = subprocess.run(cmd, capture_output=capture, text=True, check=check)
    return result.stdout.strip() if capture else None


def get_current_branch():
    return run(["git", "rev-parse", "--abbrev-ref", "HEAD"])


def get_head_commit():
    return run(["git", "rev-parse", "HEAD"])


def get_open_pr(branch):
    out = run(["gh", "pr", "view", branch, "--json", "number", "--jq", ".number"], check=False)
    if not out:
        return None
    return out


def md5sum(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <review_file.md>", file=sys.stderr)
        sys.exit(1)

    review_file = os.path.abspath(sys.argv[1])
    if not os.path.isfile(review_file):
        print(f"Review file not found: {review_file}", file=sys.stderr)
        sys.exit(1)

    if not os.path.isfile(PROMPT_FILE):
        print(f"Prompt file not found: {PROMPT_FILE}", file=sys.stderr)
        sys.exit(1)

    working_dir = os.getcwd()
    branch = get_current_branch()
    pr_number = get_open_pr(branch)
    current_commit = get_head_commit()
    current_hash = md5sum(review_file)

    if not pr_number:
        print(f"No open PR found for branch '{branch}'", file=sys.stderr)
        sys.exit(1)

    print(f"RALPH Coder started")
    print(f"  working_dir:    {working_dir}")
    print(f"  branch:         {branch}")
    print(f"  pr:             #{pr_number}")
    print(f"  current_commit: {current_commit}")
    print(f"  review_file:    {review_file}")
    print(f"  review_hash:    {current_hash}")
    print(f"  prompt:         {PROMPT_FILE}")

    while True:
        new_hash = md5sum(review_file)

        if new_hash == current_hash:
            print(f"[{time.strftime('%H:%M:%S')}] Review file unchanged. Sleeping {POLL_INTERVAL}s...")
            time.sleep(POLL_INTERVAL)
            continue

        print(f"[{time.strftime('%H:%M:%S')}] Review file changed: {current_hash[:8]} -> {new_hash[:8]}")
        current_hash = new_hash

        subprocess.run(
            ["claude", "--print", "--prompt-file", PROMPT_FILE],
            cwd=working_dir,
        )

        print(f"[{time.strftime('%H:%M:%S')}] Cleanup complete. Resuming watch...")


if __name__ == "__main__":
    main()
