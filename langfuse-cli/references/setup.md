# Local CLI setup

## Installation

Official package: `langfuse-cli`. Install user-locally so `langfuse` lands on PATH without changing system npm directories:

```bash
npm install -g --prefix ~/.local langfuse-cli
langfuse --help
```

This repository does not wrap, fork, or reimplement the CLI.

## Credentials

CLI reads project API keys and host from environment variables. Local setup stores them in `~/.config/langfuse/env` with mode `600`:

```dotenv
LANGFUSE_PUBLIC_KEY=pk-lf-XXXX
LANGFUSE_SECRET_KEY=sk-lf-XXXX
LANGFUSE_HOST=https://langfuse.example.com
LANGFUSE_BASE_URL=https://langfuse.example.com
```

Use both host variable names because official CLI accepts either while Langfuse SDKs may prefer `LANGFUSE_BASE_URL`.

```bash
langfuse --env ~/.config/langfuse/env api __schema
langfuse --env ~/.config/langfuse/env api traces list --limit 5 --json
```

Credentials are project-scoped. Never commit the env file, paste secret keys into chat, or pass keys as command-line flags. Rotate compromised keys in project settings.

## Local source

On this machine, copy the active, uncommented `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, and `LANGFUSE_HOST` values from `~/Code/writer-monorepo/backend/.env` into the local CLI env file. Ignore commented example or alternate-environment blocks. Host, project identifiers, and secret values are intentionally omitted from this public repository.

## Troubleshooting

```bash
command -v langfuse
npm list -g --prefix ~/.local --depth=0 langfuse-cli
langfuse --env ~/.config/langfuse/env api __schema
langfuse --env ~/.config/langfuse/env api traces --help
```

Authentication failure usually means wrong host/key pairing, expired or rotated keys, or keys from another project. Check presence and file permissions without printing values:

```bash
stat -f '%Sp %N' ~/.config/langfuse/env
sed -E 's/=.*/=<redacted>/' ~/.config/langfuse/env
```
