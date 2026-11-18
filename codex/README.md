# Codex in Docker

Build and launch from any directory:

```bash
~/agents/codex/build
~/agents/codex/run login --device-auth
~/agents/codex/run
```

Start Docker Desktop or `colima start` first. Device login opens a link on your
host browser; you may need to enable device code login in ChatGPT security
settings. See [official Codex authentication documentation](https://developers.openai.com/codex/auth#login-on-headless-devices).

If device code sign-in is unavailable, reuse an existing host login by copying
its file into the Docker volume once:

```bash
~/agents/codex/run --shell -c 'umask 077; cat > "$CODEX_HOME/auth.json"; chmod 600 "$CODEX_HOME/auth.json"' < ~/.codex/auth.json
~/agents/codex/run login status
```

This copies the login file; it never mounts the host config directory. The
container keeps its own copy in the persistent home volume. The host login
must be stored in `~/.codex/auth.json` for this command to work. If it lives
only in the macOS keychain, first sign in using the host Codex executable with
`-c 'cli_auth_credentials_store="file"' login` (use the actual executable rather
than the Docker alias). Keep `auth.json` out of repositories and shared logs.

To make `codex` invoke this wrapper in your shell, add this to `~/.zshrc`
(or `~/.bashrc`), then open a new terminal:

```bash
alias codex="$HOME/agents/codex/run"
```

| Host | Container | Access |
| --- | --- | --- |
| `~/agents` | `/agents` | Read-only |
| `~/reviews` | `/reviews` | Writable; created if missing |
| Current launch directory | `/workdir` | Writable; read-only if it overlaps `~/agents` or is `/` |
| Docker volume `codex-sandbox-home` | `/home/sandbox` | Writable; persists login, sessions, caches, installed dependencies |

The working directory is `/workdir` inside the container. Mounts are fixed by
the launcher; Codex arguments cannot change Docker options. Overlapping host
agents/reviews directories are rejected so the reviews mount cannot expose
`~/agents`. The `/workdir` mount is read-only if the launch directory contains
`~/agents`, is inside it, or is `/`.

All normal CLI arguments pass through, including:

```bash
codex --model MODEL_NAME
codex --cd /reviews             # Start in the writable reviews directory instead
codex exec --skip-git-repo-check 'Inspect /agents and write a report in /reviews'
codex resume --last
codex --shell                   # Open Bash inside the same container boundary
codex --shell -c 'git --version && python --version && node --version'
```

Use container paths for `--cd`, images, and output files. Code to modify must be
placed in `/reviews` or launched from its project directory to use `/workdir`;
`/agents` is for reference. Host Git/SSH
credentials are not imported. Use `codex --shell`
then `gh auth login` for private repositories; its credentials persist in the
container home volume. Files in the home volume survive subsequent launches;
other container files are discarded at exit. Python tooling has a preinstalled
virtual environment. Create writable project environments with `uv` or
`python -m venv .venv` before installing project dependencies.

Included tools: Codex CLI, Git, GitHub CLI, SSH client, Node.js/npm, TypeScript,
Python/pip/venv, uv, ruff, pytest, mypy, Go, Rust/Cargo, GCC/G++, Make, CMake,
pkg-config, curl, jq, ripgrep, fd (`fdfind`), rsync, zip/unzip, and ShellCheck.
Project-specific tooling can be installed in the writable home or review
directory. System packages must be added to the Dockerfile and rebuilt.

The image runs as your host UID/GID, drops Linux capabilities, prevents
privilege escalation, and has a read-only system filesystem. There is no Docker
socket, host home mount, SSH agent forwarding, or published port. Network access
is enabled for Codex and dependencies; this is filesystem isolation, not a
network firewall. Read-only files can still be read and sent over the network.
Anything inside the writable review directory, writable current directory, or
home volume can be changed or deleted. Docker is an isolation boundary, not a guarantee against all
container escapes.

Codex uses `approval_policy = "never"` and `sandbox_mode = "danger-full-access"`
inside the container. On each launch, `run` copies your host `config.toml` and
any `*.config.toml` profile files into the Docker home volume using a tar stream.
The host config directory is never mounted, and your original files are never
modified. The container copy overrides sandbox mode, approval policy, and
credential storage (`file`, since the macOS keychain is unavailable). The same
settings are also applied as CLI overrides, which take precedence over copied
profiles. Other settings, comments, and profile contents are preserved.
Host-specific absolute paths and macOS-only commands are copied as written;
they need container paths or Linux equivalents to work here. Skills, plugins,
login credentials, and session history are not included in this config copy.
If the host has no config, the container uses the default execution settings.
See [official configuration precedence](https://developers.openai.com/codex/config-basic).

The wrapper never invokes host Codex. The build context only includes the
Dockerfile, entrypoint, config importer, and default config, never project code
or host credentials. Copied config is stored in the volume, not baked into the
image.

Optional environment variables:

| Variable | Default | Purpose |
| --- | --- | --- |
| `CODEX_IMAGE` | `codex-sandbox:local` | Image name for both scripts |
| `CODEX_VERSION` | `0.159.3` | CLI version installed by `build`; matches the host CLI at setup |
| `CODEX_AGENTS_DIR` | `~/agents` | Read-only host directory |
| `CODEX_REVIEW_DIR` | `~/reviews` | Writable host directory |
| `CODEX_HOME_VOLUME` | `codex-sandbox-home` | Docker volume name for container home |
| `CODEX_HOST_HOME` | Host `$CODEX_HOME`, otherwise `~/.codex` | Directory to copy config and profiles from |

`build` also accepts Docker build flags, for example `~/agents/codex/build --pull`.
Rebuild for a different host user, and use a fresh home volume if its stored
permissions belong to another UID/GID. To update Codex, build with
`CODEX_VERSION=<version> ~/agents/codex/build`.

## Colima fails to start with a disk lock

If `~/.colima/_lima/colima/ha.stderr.log` reports
`failed to run attach disk "colima", in use by instance "colima"`, check:

```bash
LIMA_HOME="$HOME/.colima/_lima" limactl list
LIMA_HOME="$HOME/.colima/_lima" limactl disk list
```

If the instance is stopped but the disk is still marked in use, clear the stale
lock and start it again:

```bash
LIMA_HOME="$HOME/.colima/_lima" limactl disk unlock colima
colima start
```

Only unlock a disk after confirming its VM has stopped. This preserves the VM
disk, images, and volumes. See [Lima disk recovery documentation](https://lima-vm.io/docs/reference/limactl_disk_unlock/).
