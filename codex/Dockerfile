FROM node:22-bookworm-slim

ARG CODEX_VERSION=0.159.3
ARG SANDBOX_UID=1000
ARG SANDBOX_GID=1000

RUN apt-get update && apt-get install -y --no-install-recommends \
    bash build-essential ca-certificates cargo cmake curl fd-find git gh \
    golang jq less openssh-client patch pkg-config python3 python3-pip \
    python3-venv ripgrep rsync rustc shellcheck unzip zip \
    && rm -rf /var/lib/apt/lists/*
RUN npm install --global "@openai/codex@${CODEX_VERSION}" typescript \
    && npm cache clean --force
RUN python3 -m venv /opt/python \
    && /opt/python/bin/pip install --no-cache-dir uv ruff pytest pytest-cov mypy tomlkit

RUN groupadd --non-unique --gid "${SANDBOX_GID}" sandbox \
    && useradd --non-unique --uid "${SANDBOX_UID}" --gid sandbox \
        --create-home --shell /bin/bash sandbox \
    && mkdir -p /home/sandbox/.codex /agents /reviews /workdir \
    && chown sandbox:sandbox /reviews /workdir

COPY config.toml /home/sandbox/.codex/config.toml
COPY entrypoint /usr/local/bin/codex-entrypoint
COPY import-config /usr/local/bin/codex-import-config
RUN chmod 755 /usr/local/bin/codex-entrypoint /usr/local/bin/codex-import-config \
    && chown -R sandbox:sandbox /home/sandbox

ENV HOME=/home/sandbox \
    CODEX_HOME=/home/sandbox/.codex \
    PATH=/home/sandbox/.local/bin:/opt/python/bin:$PATH \
    UV_PYTHON_INSTALL_DIR=/home/sandbox/.local/share/uv/python
USER sandbox
WORKDIR /workdir
ENTRYPOINT ["/usr/local/bin/codex-entrypoint"]
