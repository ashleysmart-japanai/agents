# Graphify for Codex and Claude Code

- Install the official `graphifyy` package; its executable is `graphify`.
- Keep the executable global and each code graph local to its repository.
- Use the gated skill in this repository for explicit architecture, impact, and ontology-enhanced review requests.
- Keep ordinary edits and ordinary reviews on their existing workflow.

## Install the CLI on macOS

- Use Python 3.10 or later.
- Create an isolated environment with your compatible Python executable.

```bash
/opt/homebrew/bin/python3.13 -m venv "$HOME/.local/share/graphify/venv"
"$HOME/.local/share/graphify/venv/bin/python" -m pip install 'graphifyy==0.9.97'
mkdir -p "$HOME/.local/bin"
ln -s "$HOME/.local/share/graphify/venv/bin/graphify" "$HOME/.local/bin/graphify"
```

- Replace `/opt/homebrew/bin/python3.13` with your compatible interpreter on another Mac.
- Preserve an existing `~/.local/bin/graphify` installation instead of replacing it blindly.
- Add `export PATH="$HOME/.local/bin:$PATH"` to the profile of your interactive shell if that directory is missing from PATH.
- Use the absolute executable path when an IDE agent does not inherit your shell profile.

## Register the gated skill

- Run these commands from the checkout containing this file, normally `~/agents`.
- PR #14 is on `docs/fde-ds-work-tools`.
- The current PR worktree is `~/agents-pr14` while `~/agents` retains unrelated uncommitted work.
- Inspect existing skill directories before copying over a prior installation.

```bash
mkdir -p "$HOME/.agents/skills/graphify" "$HOME/.claude/skills/graphify"
cp -R skills/graphify/. "$HOME/.agents/skills/graphify/"
cp -R skills/graphify/. "$HOME/.claude/skills/graphify/"
install -m 755 bin/index-code "$HOME/.local/bin/index-code"
```

- Current Codex documentation lists `~/.agents/skills` as the user skill directory.
- This machine also loads skills from `~/.codex/skills`; copy the same skill there when using that runtime instead of creating an unrelated XDG configuration.
- Each skill uses a `SKILL.md` file with YAML `name` and `description` metadata.
- Restart the client if the skill does not appear.
- The managed environment blocked writes to this Mac's Codex discovery directories during setup.
- Claude registration and the CLI installation succeeded.
- Complete Codex registration from a normal terminal using the commands below.

```bash
mkdir -p "$HOME/.codex/skills/graphify"
cp -R skills/graphify/. "$HOME/.codex/skills/graphify/"
```

- Invoke `$graphify` in Codex or `/graphify` in Claude Code.
- Keep this custom skill when upgrading the package.
- Avoid the upstream assistant installers for this gated setup; they can add graph-first instructions or hooks.
- Remove existing Graphify-specific `PreToolUse` entries from Claude settings if a previous installation added them.
- Preserve unrelated hooks.
- Keep settings as valid JSON; JSON does not support comments.
- Remove conflicting Graphify graph-first blocks from project instruction files if a previous installation added them.

## Index and query

- Run `index-code` from the intended repository root.
- The helper calls `graphify extract . --code-only`.
- The verified CLI does not use the proposed `graphify index .` command.
- Code-only extraction skips semantic document/media processing.
- Graphify writes `graphify-out/graph.json` under the indexed directory.
- Refresh the index after source changes before relying on impact analysis.

```bash
index-code
graphify query "Which callers depend on ChangedSymbol?" --budget 2000
graphify explain "ChangedSymbol"
graphify affected "ChangedSymbol" --depth 2 --relation calls
```

## Review usage

- Request `/acs-review with KG-enhanced cross-module impact analysis` to combine the existing review method with the gated graph workflow.
- Request an ontology-enhanced review to compare documented domain invariants with implementation paths.
- Supply or locate domain definitions; extracted call relationships do not define a business ontology.
- Keep ordinary `/acs-review` graph-free unless graph analysis is explicitly requested.
- Use current source and tests as finding evidence.
- Treat missing graph edges as coverage gaps.
- The shared review method links the graph workflow at its caller-tracing stage.

## Verification

```bash
"$HOME/.local/bin/graphify" --version
"$HOME/.local/bin/graphify" --help
test -f "$HOME/.agents/skills/graphify/SKILL.md"
test -f "$HOME/.claude/skills/graphify/SKILL.md"
```

- Smoke-test indexing and querying in a disposable repository before indexing a large workspace.
- Verify that a local edit leaves the graph untouched.
- Verify that an explicit impact-analysis request queries the graph and checks source evidence.

## Sources

- [Graphify installation](https://docs.graphify.com/open-source/installation).
- [Graphify CLI reference](https://docs.graphify.com/open-source/configuration/cli).
- [Codex skill discovery](https://learn.chatgpt.com/docs/build-skills).
