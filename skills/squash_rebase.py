#!/usr/bin/env python3
"""squash_rebase.py — squash a PR branch to one commit, then rebase it onto origin/main.

Procedure (squash BEFORE rebase — the order is the point):
  1. Identify the PR branch and the target base (origin/main).
  2. Find the branch root in main's history: squash_base = merge-base(origin/main, HEAD).
  3. Squash all branch commits down onto squash_base. Zero conflicts possible there, and the
     result is checked 1:1 against the original (tree + file list + per-file line counts).
  4. Rebase the single squashed commit onto the tip of origin/main — at most ONE conflict
     round. A conflict here is EXPECTED whenever main touched the same files.

On a rebase conflict the script exits 3 and leaves the rebase in progress:
  resolve the conflicts, `git add`, `git rebase --continue`, then RE-RUN this script.
The re-run finds the pre-squash record (saved in .git/squash-rebase-intent.json), verifies
the result, reports the file/line drift the resolution caused, and pushes.

Checks:
  - before vs after squash: tree, file list, and per-file +/- line counts must match 100%,
    or the branch is restored and the script aborts.
  - after rebase: merge-base == origin/main tip, exactly 1 commit above main, and any diff
    drift the rebase caused is reported before push.

Usage:
  python3 squash_rebase.py --repo PATH [--branch NAME] [--push] [--yes]
      [--remote origin] [--main main] [--message TEXT | --message-file F] [--no-fetch]

Without --push it stops right before pushing and prints the push command (safe default).

Exit codes: 0 ok · 1 check failed (branch restored, nothing pushed) · 2 bad usage/state ·
            3 rebase conflict (resolve, `git rebase --continue`, re-run)
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile


class Abort(Exception):
    """Violated invariant — message printed, exit 1."""


def git(repo, *args, check=True):
    r = subprocess.run(["git", "-C", repo, *args], text=True, capture_output=True)
    if check and r.returncode != 0:
        raise Abort(f"git {' '.join(args)} failed:\n{(r.stderr or r.stdout).strip()}")
    return (r.stdout or "").strip()


def numstat(repo, base, head):
    """{path: '+added/-deleted'} for diff base..head ('-' counts mean binary)."""
    out = {}
    for line in git(repo, "diff", "--numstat", base, head).splitlines():
        added, deleted, path = line.split("\t", 2)
        out[path] = f"+{added}/-{deleted}"
    return out


def drift_report(intended, actual):
    """Human-readable lines for every path whose +/- counts differ between the two records."""
    lines = []
    for path in sorted(set(intended) | set(actual)):
        a, b = intended.get(path), actual.get(path)
        if a == b:
            continue
        if a is None:
            lines.append(f"  new after rebase : {path} ({b})")
        elif b is None:
            lines.append(f"  gone after rebase: {path} (was {a})")
        else:
            lines.append(f"  changed          : {path} ({a} -> {b})")
    return lines


def ensure_clean(repo):
    untracked = git(repo, "ls-files", "--others", "--exclude-standard")
    if untracked:
        raise Abort("untracked files present — refusing to rewrite history:\n" + untracked)
    stashes = git(repo, "stash", "list")
    if stashes:
        raise Abort("stashes present — refusing to rewrite history:\n" + stashes)
    status = git(repo, "status", "--short")
    if status:
        raise Abort("uncommitted changes present — commit or stash first:\n" + status)


def derive_message(repo, base, explicit, message_file):
    if message_file:
        with open(message_file) as fh:
            return fh.read().strip()
    if explicit:
        return explicit
    subjects = [s for s in git(repo, "log", "--reverse", "--format=%s", f"{base}..HEAD").splitlines() if s]
    if not subjects:
        raise Abort("no commits found to squash")
    if len(subjects) == 1:
        return subjects[0]
    return subjects[0] + "\n\nSquashed commits:\n" + "\n".join(f"- {s}" for s in subjects)


def load_intent(path, branch):
    if not os.path.exists(path):
        return None
    with open(path) as fh:
        data = json.load(fh)
    return data if data.get("branch") == branch else None


def save_intent(path, branch, original_tip, files):
    with open(path, "w") as fh:
        json.dump({"branch": branch, "original_tip": original_tip, "files": files}, fh, indent=1)


def restore(repo, tip):
    git(repo, "reset", "--hard", tip, check=False)


def main():
    ap = argparse.ArgumentParser(description="Squash a PR branch to one commit, then rebase it onto main. Safe by default.")
    ap.add_argument("--repo", default=os.getcwd())
    ap.add_argument("--remote", default="origin")
    ap.add_argument("--main", default="main")
    ap.add_argument("--branch", default=None)
    ap.add_argument("--message", default=None)
    ap.add_argument("--message-file", default=None)
    ap.add_argument("--no-fetch", action="store_true")
    ap.add_argument("--push", action="store_true")
    ap.add_argument("--yes", action="store_true")
    args = ap.parse_args()

    repo = os.path.abspath(args.repo)
    main_ref = f"{args.remote}/{args.main}"

    probe = subprocess.run(["git", "-C", repo, "rev-parse", "--absolute-git-dir"], text=True, capture_output=True)
    if probe.returncode != 0:
        print(f"ERROR: {repo} is not a git repository", file=sys.stderr)
        return 2
    gitdir = probe.stdout.strip()

    if os.path.isdir(os.path.join(gitdir, "rebase-merge")) or os.path.isdir(os.path.join(gitdir, "rebase-apply")):
        print("a rebase is already in progress — resolve conflicts, `git add` them,", file=sys.stderr)
        print(f"run `git -C {repo} rebase --continue`, then re-run this script.", file=sys.stderr)
        return 2

    try:
        ensure_clean(repo)

        branch = args.branch or git(repo, "branch", "--show-current")
        if not branch:
            raise Abort("detached HEAD — pass --branch")
        if branch == args.main:
            raise Abort(f"refusing to run on '{args.main}' itself; check out the PR branch")
        if git(repo, "branch", "--show-current") != branch:
            git(repo, "checkout", branch)

        if not args.no_fetch:
            git(repo, "fetch", "--prune", args.remote)
        if not git(repo, "rev-parse", "--verify", "--quiet", main_ref, check=False):
            raise Abort(f"{main_ref} does not exist")

        head = git(repo, "rev-parse", "HEAD")
        main_tip = git(repo, "rev-parse", main_ref)
        squash_base = git(repo, "merge-base", main_ref, "HEAD")  # step 2: the "squash hash"
        count = int(git(repo, "rev-list", "--count", f"{squash_base}..HEAD"))
        if count == 0:
            raise Abort("no commits above the merge-base — nothing to squash")

        # Pre-squash record of the intended diff (files + per-file line counts).
        # If the branch is already a single commit and a record exists (conflict re-run), reuse it.
        intent_path = os.path.join(gitdir, "squash-rebase-intent.json")
        intent = load_intent(intent_path, branch) if count == 1 else None
        if intent:
            intended, original_tip = intent["files"], intent["original_tip"]
            print(f"resuming with pre-squash record from {intent_path}")
        else:
            intended, original_tip = numstat(repo, squash_base, "HEAD"), head
            if not intended:
                raise Abort("empty diff vs merge-base — nothing to do")
            save_intent(intent_path, branch, original_tip, intended)

        print("=" * 70)
        print(f"branch      : {branch}")
        print(f"{main_ref} tip : {main_tip}")
        print(f"squash base : {squash_base}" + ("  (== main tip, no rebase needed)" if squash_base == main_tip else ""))
        print(f"commits     : {count} to squash")
        print(f"files       : {len(intended)}")
        print(f"recovery    : git -C {repo} reset --hard {original_tip}")
        print("=" * 70)

        if not args.yes:
            if input("proceed with squash + rebase? [y/N] ").strip().lower() not in ("y", "yes"):
                print("aborted by user — nothing changed")
                return 0

        # --- step 3: squash to the squash hash, then verify a 100% match ---
        if count > 1:
            tree_before = git(repo, "rev-parse", "HEAD^{tree}")
            message = derive_message(repo, squash_base, args.message, args.message_file)
            git(repo, "reset", "--soft", squash_base)
            fd, msg_path = tempfile.mkstemp(prefix="squash-rebase-msg-", suffix=".txt")
            with os.fdopen(fd, "w") as fh:
                fh.write(message + "\n")
            try:
                git(repo, "commit", "-F", msg_path)
            finally:
                os.unlink(msg_path)

            failure = None
            if git(repo, "rev-parse", "HEAD^{tree}") != tree_before:
                failure = "tree differs"
            elif numstat(repo, squash_base, "HEAD") != intended:
                failure = "file list / line counts differ"
            elif git(repo, "rev-list", "--count", f"{squash_base}..HEAD") != "1":
                failure = "not exactly 1 commit"
            if failure:
                restore(repo, original_tip)
                raise Abort(f"post-squash check failed ({failure}) — branch restored to {original_tip}")
            print(f"[squash ok] {count} commits -> 1; tree, file list, and line counts match 100%")

        # --- step 4: rebase the single squashed commit onto the target tip ---
        if squash_base != main_tip:
            print(f"rebasing squashed commit onto {main_ref} ({main_tip}) ...")
            try:
                git(repo, "rebase", "--onto", main_ref, squash_base)
            except Abort:
                conflicted = git(repo, "diff", "--name-only", "--diff-filter=U", check=False)
                print("\nCONFLICT — expected when main touched the same files. Rebase left in progress.")
                print("conflicted files:\n" + "\n".join(f"  {f}" for f in conflicted.splitlines()))
                print("\nnext steps:")
                print(f"  1. resolve the conflicts, then `git -C {repo} add <files>`")
                print(f"  2. git -C {repo} rebase --continue")
                print("  3. re-run this script — it verifies the result, reports rebase-caused drift, and pushes")
                print(f"to give up instead: git -C {repo} rebase --abort && git -C {repo} reset --hard {original_tip}")
                return 3

        # --- post-rebase checks + drift report ---
        if git(repo, "merge-base", main_ref, "HEAD") != main_tip:
            restore(repo, original_tip)
            raise Abort("merge-base did not advance to the main tip after rebase — branch restored")
        if git(repo, "rev-list", "--count", f"{main_ref}..HEAD") != "1":
            restore(repo, original_tip)
            raise Abort("expected exactly 1 commit above main after rebase — branch restored")

        drift = drift_report(intended, numstat(repo, main_ref, "HEAD"))
        if drift:
            print(f"\nfile/line changes caused by the rebase ({len(drift)} paths):")
            print("\n".join(drift))
        else:
            print("\n[rebase ok] diff identical to the pre-squash record — the rebase changed nothing")

        print()
        print(git(repo, "log", "--graph", "--oneline", "-n", "5"))

        push_cmd = f"git -C {repo} push --force-with-lease {args.remote} {branch}"
        if not args.push:
            print(f"\nstopped before push (safe default). To push: {push_cmd}")
            return 0
        if drift and not args.yes:
            if input("push despite rebase-caused drift? [y/N] ").strip().lower() not in ("y", "yes"):
                print(f"not pushed. When ready: {push_cmd}")
                return 0
        print(f"\npushing: {push_cmd}")
        git(repo, "push", "--force-with-lease", args.remote, branch)
        if os.path.exists(intent_path):
            os.unlink(intent_path)
        print("pushed with --force-with-lease.")
        return 0

    except Abort as e:
        print(f"\nABORTED: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
