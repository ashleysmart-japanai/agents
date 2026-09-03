#!/usr/bin/env python3
"""RALPH Reviewer — watches a PR branch for new commits and triggers a Claude review."""

import hashlib
import os
import subprocess
import sys
import time

POLL_INTERVAL = 60
PROMPT_FILE = os.path.join(os.path.dirname(__file__), "RALPH_REVIEWER.md")


def run(cmd, *, check=True, capture=True):
    result = subprocess.run(cmd, capture_output=capture, text=True, check=check)
    return result.stdout.strip() if capture else None


def get_current_branch():
    return run(["git", "rev-parse", "--abbrev-ref", "HEAD"])


def get_head_commit():
    return run(["git", "rev-parse", "HEAD"])


def get_open_pr(branch):
    out = run(["gh", "pr", "view", branch, "--json", "number,url", "--jq", ".number"], check=False)
    if not out:
        return None
    return out


def fetch_and_pull(branch):
    run(["git", "fetch", "--all", "--prune"])
    run(["git", "pull", "--ff-only"], check=False)


def main():
    working_dir = os.getcwd()
    branch = get_current_branch()
    pr_number = get_open_pr(branch)
    current_commit = get_head_commit()

    if not pr_number:
        print(f"No open PR found for branch '{branch}'", file=sys.stderr)
        sys.exit(1)

    if not os.path.isfile(PROMPT_FILE):
        print(f"Prompt file not found: {PROMPT_FILE}", file=sys.stderr)
        sys.exit(1)

    print(f"RALPH Reviewer started")
    print(f"  working_dir:    {working_dir}")
    print(f"  branch:         {branch}")
    print(f"  pr:             #{pr_number}")
    print(f"  current_commit: {current_commit}")
    print(f"  prompt:         {PROMPT_FILE}")

    while True:
        fetch_and_pull(branch)
        new_commit = get_head_commit()

        if new_commit == current_commit:
            print(f"[{time.strftime('%H:%M:%S')}] No new commits. Sleeping {POLL_INTERVAL}s...")
            time.sleep(POLL_INTERVAL)
            continue

        print(f"[{time.strftime('%H:%M:%S')}] New commit detected: {current_commit[:8]} -> {new_commit[:8]}")
        current_commit = new_commit

        subprocess.run(
            ["claude", "--print", "--prompt-file", PROMPT_FILE],
            cwd=working_dir,
        )

        print(f"[{time.strftime('%H:%M:%S')}] Review complete. Resuming watch...")


if __name__ == "__main__":
    main()
